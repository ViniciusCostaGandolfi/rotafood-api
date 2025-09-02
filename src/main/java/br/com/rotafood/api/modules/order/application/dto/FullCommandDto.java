package br.com.rotafood.api.modules.order.application.dto;

import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.Command;
import br.com.rotafood.api.modules.order.domain.entity.CommandStatus;
import br.com.rotafood.api.modules.order.domain.entity.OrderStatus;
import jakarta.validation.constraints.NotNull;

public record FullCommandDto(
    UUID id,
    @NotNull String name,
    Integer merchantSequence,
    Integer tableIndex,
    @NotNull CommandStatus status,
    List<FullOrderDto> orders

) {
    public FullCommandDto(Command command) {
    this(
        command.getId(),
        command.getName(),
        command.getMerchantSequence(),
        command.getTableIndex(),
        command.getStatus(),
        command.getOrders() != null
            ? command.getOrders().stream()
                .filter(order -> order.getStatus() != OrderStatus.COMPLETED && order.getStatus() != OrderStatus.CANCELED)
                .map(FullOrderDto::new)
                .toList()
            : null
    );
}
}
