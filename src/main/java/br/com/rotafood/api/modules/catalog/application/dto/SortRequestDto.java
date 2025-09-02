package br.com.rotafood.api.modules.catalog.application.dto;

import java.util.UUID;

public record SortRequestDto(
    UUID id,
    Integer index
) {
    
}
