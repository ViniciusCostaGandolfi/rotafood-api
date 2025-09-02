package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.DefaultProduct;

public record DefaultProductDto(
    UUID id,
    String name,
    String description,
    String ean,
    String imagePath,
    String iFoodImagePath
) {
    public DefaultProductDto(DefaultProduct defaultProduct) {
        this(
            defaultProduct.getId(),
            defaultProduct.getName(),
            defaultProduct.getDescription(),
            defaultProduct.getEan(),
            defaultProduct.getImagePath(),
            defaultProduct.getIFoodImagePath()
        );
    }


    
}
