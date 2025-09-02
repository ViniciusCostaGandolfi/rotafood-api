package br.com.rotafood.api.modules.order.application.dto;


import java.util.Date;
import java.util.UUID;

import br.com.rotafood.api.infra.utils.DateUtils;
import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderSalesChannel;
import br.com.rotafood.api.modules.order.domain.entity.OrderStatus;
import br.com.rotafood.api.modules.order.domain.entity.OrderTiming;
import br.com.rotafood.api.modules.order.domain.entity.OrderType;

public record OrderDto(
    UUID id,
    Long merchantSequence,
    Date modifiedAt,
    Date createdAt,
    Date preparationStartDateTime,
    OrderType type,
    OrderStatus status,
    OrderSalesChannel salesChannel,
    OrderTiming timing,
    String extraInfo,
    UUID merchantId,
    OrderTotalDto total
) {
    public OrderDto(Order order) {
        this(
            order.getId(),
            order.getMerchantSequence(),
            DateUtils.convertInstantToDate(order.getModifiedAt()),
            DateUtils.convertInstantToDate(order.getCreatedAt()),
            DateUtils.convertInstantToDate(order.getPreparationStartDateTime()),
            order.getType(),
            order.getStatus(),
            order.getSalesChannel(),
            order.getTiming(),
            order.getExtraInfo(),
            order.getMerchant().getId(),
            order.getTotal() != null ? new OrderTotalDto(order.getTotal()) : null
        );
    }
}
