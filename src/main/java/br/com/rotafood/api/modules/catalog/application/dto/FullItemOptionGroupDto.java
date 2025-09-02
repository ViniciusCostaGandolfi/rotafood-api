package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.ItemOptionGroup;
import jakarta.validation.constraints.NotNull;

public record FullItemOptionGroupDto(
    UUID id,
    @NotNull
    Integer min,
    @NotNull
    Integer max,
    @NotNull
    Integer index,
    OptionGroupDto optionGroup
) {
    public FullItemOptionGroupDto(ItemOptionGroup itemOptionGroup) {
        this(
            itemOptionGroup.getId(),
            itemOptionGroup.getMin(),
            itemOptionGroup.getMax(),
            itemOptionGroup.getIndex(),
            itemOptionGroup.getOptionGroup() != null ? new OptionGroupDto(itemOptionGroup.getOptionGroup()) : null
        );
    }
}