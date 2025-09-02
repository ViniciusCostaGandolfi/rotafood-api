package br.com.rotafood.api.modules.catalog.application.service;

import br.com.rotafood.api.infra.config.minio.MinioStorageService;
import br.com.rotafood.api.modules.catalog.application.dto.ContextModifierDto;
import br.com.rotafood.api.modules.catalog.application.dto.FullCategoryDto;
import br.com.rotafood.api.modules.merchant.domain.repository.CategoryRepository;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.UUID;

import org.springframework.scheduling.annotation.Async;


@Service
public class CatalogCacheService {

    private final MinioStorageService minioStorageService;
    private final CategoryRepository categoryRepository;
    private final ObjectMapper objectMapper;

    @Value("${minio.bucket.name}")
    private String bucketName;

    public CatalogCacheService(MinioStorageService minioStorageService, CategoryRepository categoryRepository, ObjectMapper objectMapper) {
        this.minioStorageService = minioStorageService;
        this.categoryRepository = categoryRepository;
        this.objectMapper = objectMapper;
    }

    private List<FullCategoryDto> readCache(UUID merchantId) {
        String objectName = "catalogs/" + merchantId + ".json";
        try (InputStream is = minioStorageService.download(bucketName, objectName)) {
        return objectMapper.readValue(
            is,
            new TypeReference<List<FullCategoryDto>>() {}
        );
        } catch (Exception e) {
        throw new RuntimeException("Erro ao ler cache", e);
        }
    }

    private void writeCache(UUID merchantId, List<FullCategoryDto> cats) {
        try {
        String json = objectMapper.writeValueAsString(cats);
        ByteArrayInputStream in = new ByteArrayInputStream(
            json.getBytes(StandardCharsets.UTF_8)
        );
        String objectName = "catalogs/" + merchantId + ".json";
        minioStorageService.uploadFile(bucketName, objectName, in, "application/json");
        } catch (Exception e) {
        throw new RuntimeException("Erro ao escrever cache", e);
        }
    }

    @Async("virtualThreadExecutor")
    @Transactional
    public void updateCatalogCache(UUID merchantId) {
        try {
            System.out.println("⏳ Atualizando cache do catálogo do merchant " + merchantId + " em background...");
            var categories = categoryRepository.findAllByMerchantIdWithItems(merchantId)
                                    .stream()
                                    .map(FullCategoryDto::new)
                                    .toList();

            String json = objectMapper.writeValueAsString(categories);
            ByteArrayInputStream inputStream = new ByteArrayInputStream(json.getBytes(StandardCharsets.UTF_8));

            String objectName = "catalogs/" + merchantId + ".json";

            minioStorageService.uploadFile(bucketName, objectName, inputStream, "application/json");

            System.out.println("✅ Cache do catálogo atualizado para merchant " + merchantId);
        } catch (Exception e) {
            System.err.println("❌ Erro ao atualizar cache do catálogo (merchant " + merchantId + "): " + e.getMessage());
            e.printStackTrace();
        }
    }


    @Transactional
    public void updateOrCreateContextModifier(UUID merchantId,
        ContextModifierDto newMod
    ) {
        var cats = readCache(merchantId);
        for (FullCategoryDto cat : cats) {
            cat.items().stream()
                .filter(item -> item.id().equals(newMod.itemId()))
                .findFirst()
                .ifPresent(item -> {
                var mods = item.contextModifiers();
                boolean ok = false;
                for (int i = 0; i < mods.size(); i++) {
                    if (mods.get(i).id().equals(newMod.id())) {
                    mods.set(i, newMod);
                    ok = true;
                    break;
                    }
                }
                if (!ok) mods.add(newMod);
            });
        }
        writeCache(merchantId, cats);
    }

}
