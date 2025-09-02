package br.com.rotafood.api.modules.order.application.dto;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.OrderTotal;

public record OrderTotalDto(
    UUID id,
    BigDecimal benefits,
    BigDecimal deliveryFee,
    BigDecimal orderAmount,
    BigDecimal serviceFee,
    BigDecimal subTotal,
    BigDecimal additionalFees
) {
    public OrderTotalDto(OrderTotal total) {
        this(
            total.getId(),
            total.getBenefits(),
            total.getDeliveryFee(),
            total.getOrderAmount(),
            total.getSubTotal(),
            total.getServiceFee(),
            total.getAdditionalFees()
        );
    }

}

