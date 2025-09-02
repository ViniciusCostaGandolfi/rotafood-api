package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.ProductPackaging;

public record ProductPackagingDto(
    UUID id,
    Integer quantityPerPackage,
    PackagingDto packaging
) {
    public ProductPackagingDto(ProductPackaging productPackaging) {
        this(productPackaging.getId(), 
        productPackaging.getQuantityPerPackage(),
        new PackagingDto(productPackaging.getPackaging()));
    }
}