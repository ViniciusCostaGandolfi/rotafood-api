package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.ItemOptionGroup;
import jakarta.validation.constraints.NotNull;

public record ItemOptionGroupDto(
    UUID id,
    @NotNull
    Integer min,
    @NotNull
    Integer max,
    @NotNull
    Integer index,
    @NotNull
    UUID optionGroupId
) {
    public ItemOptionGroupDto(ItemOptionGroup itemOptionGroup) {
        this(
            itemOptionGroup.getId(),
            itemOptionGroup.getMin(),
            itemOptionGroup.getMax(),
            itemOptionGroup.getIndex(),
            itemOptionGroup.getOptionGroup().getId()
        );
    }
}