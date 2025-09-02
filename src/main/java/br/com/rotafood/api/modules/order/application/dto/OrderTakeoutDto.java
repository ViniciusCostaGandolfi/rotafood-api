package br.com.rotafood.api.modules.order.application.dto;

import java.util.Date;
import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.OrderTakeout;
import br.com.rotafood.api.modules.order.domain.entity.OrderTakeoutMode;

public record OrderTakeoutDto(
    UUID id,
    Date takeoutDateTime,
    OrderTakeoutMode mode,
    String comments
) {

    public OrderTakeoutDto(OrderTakeout takeout) {
        this(
            takeout.getId(),
            takeout.getTakeoutDateTime(),
            takeout.getMode(),
            takeout.getComments()
        );
    }

}

