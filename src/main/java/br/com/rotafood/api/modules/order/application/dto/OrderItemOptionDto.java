package br.com.rotafood.api.modules.order.application.dto;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.OrderItemOption;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public record OrderItemOptionDto(
    UUID id,
    @Min(1)
    int quantity,
    @Min(0)
    BigDecimal totalPrice,
    @NotNull
    UUID contextModifierId,
    @NotNull
    UUID groupId,
    @NotNull
    String groupName,
    @NotNull
    @Valid
    OrderOptionDetailDto option
) {
    public OrderItemOptionDto(OrderItemOption orderItemOption) {
        this(
            orderItemOption.getId(),
            orderItemOption.getQuantity(),
            orderItemOption.getTotalPrice(),
            orderItemOption.getContextModifier().getId(),
            orderItemOption.getOption() != null ? orderItemOption.getOption().getOptionGroup().getId() : null,
            orderItemOption.getOption() != null ? orderItemOption.getOption().getOptionGroup().getName() : null,
            orderItemOption.getOption() != null ? new OrderOptionDetailDto(orderItemOption.getOption()) : null
        );
    }

}
