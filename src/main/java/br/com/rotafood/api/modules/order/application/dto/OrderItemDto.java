package br.com.rotafood.api.modules.order.application.dto;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.OrderItem;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public record OrderItemDto(
    UUID id,
    @Min(1)
    int quantity,
    @Min(0)
    BigDecimal totalPrice,
    @Min(0)
    BigDecimal optionsPrice,
    String observations,
    @NotNull
    UUID contextModifierId,
    @Valid
    OrderItemDetailDto item,
    @Valid
    List<OrderItemOptionDto> options

) {
    public OrderItemDto(OrderItem orderItem) {
    this(
        orderItem.getId(),
        orderItem.getQuantity(),
        orderItem.getTotalPrice(),
        orderItem.getOptionsPrice(),
        orderItem.getObservations(),
        orderItem.getContextModifier().getId(),
        orderItem.getItem() != null ? new OrderItemDetailDto(orderItem.getItem()) : null,
        orderItem.getOptions() != null ? orderItem.getOptions().stream().map(OrderItemOptionDto::new).toList() : null
    );
}

}
