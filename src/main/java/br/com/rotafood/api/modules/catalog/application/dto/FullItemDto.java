package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.Item;
import br.com.rotafood.api.modules.catalog.domain.entity.TemplateType;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;


public record FullItemDto(
    UUID id,
    @NotNull
    AvailabilityStatus status,
    @NotNull
    Integer index,
    @NotNull
    TemplateType type,
    UUID categoryId,
    List<ShiftDto> shifts,
    @Valid
    List<ContextModifierDto> contextModifiers,
    @Valid
    List<FullItemOptionGroupDto> optionGroups,
    @Valid
    @NotNull
    ProductDto product
) {
    public FullItemDto(Item item) {
        this(
            item.getId(),
            item.getStatus(),
            item.getIndex(),
            item.getType(),
            item.getCategory().getId(),
            item.getShifts() != null ? item.getShifts().stream().map(ShiftDto::new).toList() : null,
            item.getContextModifiers() != null ? item.getContextModifiers().stream().map(ContextModifierDto::new).toList() : null,
            item.getItemOptionGroups() != null 
                ? item.getItemOptionGroups().stream()
                    .map(FullItemOptionGroupDto::new)
                    .toList()
                : null,  
            new ProductDto(item.getProduct())
        );
    }
}