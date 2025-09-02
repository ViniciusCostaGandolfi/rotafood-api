package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.TemplateType;
import jakarta.validation.Valid;

@Valid
public record CategoryAggregatedDto(
    UUID id,
    Integer index,
    String name,
    TemplateType template,
    AvailabilityStatus status,
    List<ItemDto> items,
    List<OptionGroupDto> optionGroups
) {
}
