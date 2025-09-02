package br.com.rotafood.api.modules.catalog.application.service;

import br.com.rotafood.api.modules.catalog.domain.entity.DefaultPackaging;
import br.com.rotafood.api.modules.merchant.domain.repository.DefaultPackagingRepository;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class DefaultPackagingPopulateService {

    @Autowired
    private DefaultPackagingRepository defaultPackagingRepository;

    public void populateDatabase(String jsonFilePath) throws IOException {

        ObjectMapper objectMapper = new ObjectMapper();
        JsonNode rootNode = objectMapper.readTree(new File(jsonFilePath));

        List<DefaultPackaging> packagings = new ArrayList<>();
        for (JsonNode node : rootNode) {
            DefaultPackaging packaging = new DefaultPackaging();

            packaging.setId(UUID.fromString(getSafeText(node, "id")));
            packaging.setName(getSafeText(node, "name"));
            packaging.setImagePath(getSafeText(node, "imagePath"));
            packaging.setIFoodImagePath(getSafeText(node, "imagePath"));
            packaging.setLenghtCm(getSafeDecimal(node, "lenghtCm"));
            packaging.setWidthCm(getSafeDecimal(node, "widthCm"));
            packaging.setThicknessCm(getSafeDecimal(node, "thicknessCm"));
            packaging.setVolumeMl(getSafeDecimal(node, "volumeMl"));

            packagings.add(packaging);
        }

        defaultPackagingRepository.saveAll(packagings);
    }

    private String getSafeText(JsonNode node, String fieldName) {
        JsonNode fieldNode = node.get(fieldName);
        return (fieldNode != null) ? fieldNode.asText() : "";
    }

    private BigDecimal getSafeDecimal(JsonNode node, String fieldName) {
        JsonNode fieldNode = node.get(fieldName);
        return (fieldNode != null) ? BigDecimal.valueOf(fieldNode.asDouble()) : BigDecimal.ZERO;
    }
}