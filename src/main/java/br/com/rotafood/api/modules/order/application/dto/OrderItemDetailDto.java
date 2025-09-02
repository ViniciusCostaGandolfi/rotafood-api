package br.com.rotafood.api.modules.order.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.Item;
import br.com.rotafood.api.modules.catalog.domain.entity.Serving;
import jakarta.validation.constraints.NotNull;

public record OrderItemDetailDto(
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
    public OrderItemDetailDto(Item itemDetail) {
        this(
            itemDetail.getId(),
            itemDetail.getProduct().getName(),
            itemDetail.getProduct().getDescription(),
            itemDetail.getProduct().getEan(),
            itemDetail.getProduct().getAdditionalInformation(),
            itemDetail.getProduct().getServing(),
            itemDetail.getProduct().getImagePath()
        );
    }
}
