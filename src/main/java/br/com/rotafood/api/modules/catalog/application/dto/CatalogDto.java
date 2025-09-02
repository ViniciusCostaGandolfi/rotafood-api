package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.Date;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.Catalog;
import br.com.rotafood.api.modules.catalog.domain.entity.CatalogContext;

public record CatalogDto(
    UUID id,
    Date modifiedAt,
    AvailabilityStatus status,
    CatalogContext catalogContext,
    UUID iFoodCatalofId
) {
    public CatalogDto(Catalog catalog) {

        this(
            catalog.getId(), 
            catalog.getModifiedAt(), 
            catalog.getStatus(), 
            catalog.getCatalogContext(),
            catalog.getIFoodCatalogId()
            );
    }
}
