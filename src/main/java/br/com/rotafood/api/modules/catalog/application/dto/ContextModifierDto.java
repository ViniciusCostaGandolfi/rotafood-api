package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.CatalogContext;
import br.com.rotafood.api.modules.catalog.domain.entity.ContextModifier;

public record ContextModifierDto(
    UUID id,
    UUID itemId,
    UUID optionId,
    UUID parentOptionId,
    AvailabilityStatus status,
    PriceDto price,
    CatalogContext catalogContext
) {
    public ContextModifierDto(ContextModifier contextModifier) {
        this(
            contextModifier.getId(),
            contextModifier.getItem() != null ? contextModifier.getItem().getId(): null,
            contextModifier.getOption() != null ? contextModifier.getOption().getId(): null,
            contextModifier.getParentOptionModifier() != null? contextModifier.getParentOptionModifier().getId() : null,
            contextModifier.getStatus(),
            new PriceDto(contextModifier.getPrice()),
            contextModifier.getCatalogContext()
        );
    }
}
