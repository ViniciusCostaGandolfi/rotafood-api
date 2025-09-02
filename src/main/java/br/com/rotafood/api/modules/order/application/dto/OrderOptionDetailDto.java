package br.com.rotafood.api.modules.order.application.dto;


import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.Option;
import br.com.rotafood.api.modules.catalog.domain.entity.Serving;
import jakarta.validation.constraints.NotNull;

public record OrderOptionDetailDto(
    @NotNull
    UUID id,
    @NotNull
    String name,
    String description,
    String ean,
    String additionalInformation,
    Serving serving,
    String imagePath
) {
    public OrderOptionDetailDto(Option option) {
        this(
            option.getId(),
            option.getProduct().getName(),
            option.getProduct().getDescription(),
            option.getProduct().getEan(),
            option.getProduct().getAdditionalInformation(),
            option.getProduct().getServing(),
            option.getProduct().getImagePath()
        );
    }
    
}
