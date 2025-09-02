package br.com.rotafood.api.modules.order.application.dto;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.OrderAdditionalFee;


public record OrderAdditionalFeeDto(
    UUID id,
    String type,
    BigDecimal value,
    String name,
    String description
) {
    public OrderAdditionalFeeDto(OrderAdditionalFee additionalFee) {
    this(
        additionalFee.getId(),
        additionalFee.getType(),
        additionalFee.getValue(),
        additionalFee.getName(),
        additionalFee.getDescription()
    );
}

}