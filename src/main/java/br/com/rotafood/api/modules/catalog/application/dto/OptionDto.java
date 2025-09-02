package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.Option;
import jakarta.validation.constraints.NotNull;

public record OptionDto (
    UUID id,
    @NotNull
    AvailabilityStatus status,
    @NotNull
    Integer index,
    List<ContextModifierDto> contextModifiers,
    List<Integer> fractions,
    ProductDto product
) {
    public OptionDto(Option option) {
        this(
            option.getId(),
            option.getStatus(),
            option.getIndex(),
            option.getContextModifiers() != null ? option.getContextModifiers().stream().map(ContextModifierDto::new).toList() : null,
            option.getFractions() != null ? option.getFractions() : null,
            option.getProduct() != null ? new ProductDto(option.getProduct()) : null
        );
    }
}
