package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.Category;
import br.com.rotafood.api.modules.catalog.domain.entity.TemplateType;

public record FullCategoryDto(
    UUID id,
    Integer index,
    String name, 
    TemplateType template,
    AvailabilityStatus status,
    List<FullItemDto> items
) {
    public FullCategoryDto(Category category) {
        this(
            category.getId(),
            category.getIndex(),
            category.getName(),
            category.getTemplate(),
            category.getStatus(),
            category.getItems().stream()
            .sorted((a, b) -> {
                if (a.getIndex() == null && b.getIndex() == null) return 0;
                if (a.getIndex() == null) return 1;
                if (b.getIndex() == null) return -1;
                return Integer.compare(a.getIndex(), b.getIndex());
            })
            .map(FullItemDto::new)
            .toList()
    );
    }
}
