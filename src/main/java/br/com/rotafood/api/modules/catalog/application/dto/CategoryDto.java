package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.Category;
import br.com.rotafood.api.modules.catalog.domain.entity.TemplateType;

public record CategoryDto(
    UUID id,
    Integer index,
    String name,
    TemplateType template,
    AvailabilityStatus status
    ) {
    public CategoryDto(Category category) {
        this(
            category.getId(),
            category.getIndex(),
            category.getName(),
            category.getTemplate(),
            category.getStatus()        
            );
    }
}
