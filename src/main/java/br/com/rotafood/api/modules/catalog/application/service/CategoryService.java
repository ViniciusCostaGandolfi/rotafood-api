package br.com.rotafood.api.modules.catalog.application.service;

import java.io.InputStream;
import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import br.com.rotafood.api.infra.config.minio.MinioStorageService;
import br.com.rotafood.api.modules.catalog.application.dto.CategoryDto;
import br.com.rotafood.api.modules.catalog.application.dto.FullCategoryDto;
import br.com.rotafood.api.modules.catalog.application.dto.SortRequestDto;
import br.com.rotafood.api.modules.catalog.domain.entity.Category;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.CategoryRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.ItemRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import jakarta.persistence.EntityNotFoundException;

@Service
public class CategoryService {

    @Autowired 
    private CategoryRepository categoryRepository;
    
    @Autowired 
    private MerchantRepository merchantRepository;
    
    @Autowired 
    private ItemRepository itemRepository;
    
    @Autowired 
    private MinioStorageService  minioService;
    
    @Autowired 
    private ObjectMapper  objectMapper;
    
    @Value("${minio.url}") 
    private String minioUrl;
    
    @Value("${minio.bucket.name}") 
    private String minioBucketName;



    public Category getByIdAndMerchantId(UUID categoryId, UUID merchantId) {
        return categoryRepository.findByIdAndMerchantId(categoryId, merchantId);
    }

    @Transactional
    public void deleteByIdAndMerchantId(UUID categoryId, UUID merchantId) {
        Category category = categoryRepository.findByIdAndMerchantId(categoryId, merchantId);

        if (category == null) {
            throw new EntityNotFoundException("Categoria não encontrada.");
        }
        categoryRepository.delete(category);
    }


    public List<Category> getAllByMerchantId(UUID merchantId) {
        return categoryRepository.findAllByMerchantIdWithItems(merchantId);
    }

    @Transactional(readOnly = true)
    public List<FullCategoryDto> getAllByMerchantIdFromBucket(UUID merchantId) {
        String objectName = "catalogs/" + merchantId + ".json";
        try (InputStream is = minioService.download(minioBucketName, objectName)) {
            return objectMapper.readValue(
                is,
                new TypeReference<List<FullCategoryDto>>() {}
            );
        } catch (Exception e) {
            System.err.println("Não foi possível ler o catálogo para merchant " + merchantId + ": " + e.getMessage());

             return categoryRepository
                    .findAllByMerchantIdWithItems(merchantId)
                    .stream()
                    .map(FullCategoryDto::new)
                    .toList();

        }
    }



    @Transactional
    public Category updateOrCreate(CategoryDto categoryDto, UUID merchantId) {
        Merchant merchant = merchantRepository.findById(merchantId)
                .orElseThrow(() -> new EntityNotFoundException("Merchant não encontrado."));

        Category category = categoryDto.id() != null
                ? categoryRepository.findByIdAndMerchantId(categoryDto.id(), merchantId)
                : new Category();

        category.setName(categoryDto.name());
        category.setTemplate(categoryDto.template());
        category.setStatus(categoryDto.status());
        category.setMerchant(merchant);

        List<Category> categories = categoryRepository.findAllByMerchantId(merchantId);

        int newIndex = categoryDto.index() == -1 
                ? categories.stream().map(Category::getIndex).max(Integer::compareTo).orElse(0) + 1
                : categoryDto.index();

        category.setIndex(newIndex + 1);

        Category savedCategory = categoryRepository.save(category);

        return savedCategory;
    }

    @Transactional
    public void sortItemsInCategory(UUID merchantId, UUID categoryId, List<SortRequestDto> sortedItems) {
        sortedItems.forEach(dto -> 
            itemRepository.updateItemIndex(categoryId, dto.id(), dto.index()));
    }

    @Transactional
    public void sortCategories(UUID merchantId, List<SortRequestDto> sortedCategories) {

        sortedCategories.forEach(dto -> 
            {
                categoryRepository.updateCategoryIndex(merchantId, dto.id(), dto.index());
            });
    }
}