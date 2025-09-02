package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.Comparator;
import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.Option;
import br.com.rotafood.api.modules.catalog.domain.entity.OptionGroup;
import br.com.rotafood.api.modules.catalog.domain.entity.OptionGroupType;

public record OptionGroupDto(
    UUID id,
    String name,
    AvailabilityStatus status,
    OptionGroupType optionGroupType,
    List<OptionDto> options,
    UUID iFoodOptionGroupId
) {
    public OptionGroupDto(OptionGroup optionGroup) {
        this(
            optionGroup.getId(),
            optionGroup.getName(),
            optionGroup.getStatus(),
            optionGroup.getOptionGroupType(),
            optionGroup.getOptions().stream()
                .sorted(Comparator
                    .comparing(Option::getIndex)
                    .thenComparing(o -> o.getId().toString()))
                .map(OptionDto::new)
                .toList(),
            optionGroup.getIFoodOptionGroupId()
        );
    }
}
