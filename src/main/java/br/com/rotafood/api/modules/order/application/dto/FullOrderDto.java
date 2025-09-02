package br.com.rotafood.api.modules.order.application.dto;

import java.util.Date;
import java.util.List;
import java.util.UUID;
import java.util.Optional;

import br.com.rotafood.api.infra.utils.DateUtils;
import br.com.rotafood.api.modules.common.application.dto.CustomerDto;
import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderSalesChannel;
import br.com.rotafood.api.modules.order.domain.entity.OrderStatus;
import br.com.rotafood.api.modules.order.domain.entity.OrderTiming;
import br.com.rotafood.api.modules.order.domain.entity.OrderType;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;


public record FullOrderDto(
    UUID id,
    Long merchantSequence,
    Date modifiedAt,
    Date createdAt,
    @NotNull
    Date preparationStartDateTime,
    @NotNull
    OrderType type,
    @NotNull
    OrderStatus status,
    @NotNull
    OrderSalesChannel salesChannel,
    @NotNull
    OrderTiming timing,
    String extraInfo,
    boolean printed,
    @NotNull
    UUID merchantId,
    OrderTotalDto total,
    @Valid
    CustomerDto customer,
    @Valid
    OrderDeliveryDto delivery,
    @Valid
    OrderScheduleDto schedule,
    @Valid
    OrderTakeoutDto takeout,
    @Valid
    CommandDto command,
    @Valid
    @NotNull
    PaymentRecordDto payment, 
    @Valid
    @NotEmpty
    List<OrderItemDto> items,
    List<OrderBenefitDto> benefits,
    List<OrderAdditionalFeeDto> additionalFees
) {
    public FullOrderDto(Order order) {
         this( order.getId(),
         order.getMerchantSequence(),
         DateUtils.convertInstantToDate(order.getModifiedAt()),
         DateUtils.convertInstantToDate(order.getCreatedAt()),
         DateUtils.convertInstantToDate(order.getPreparationStartDateTime()),
         order.getType(),
         order.getStatus(),
         order.getSalesChannel(),
         order.getTiming(),
         order.getExtraInfo(),
         order.isPrinted(),
         order.getMerchant().getId(),
         Optional.ofNullable(order.getTotal()).map(OrderTotalDto::new).orElse(null),
         Optional.ofNullable(order.getCustomer()).map(CustomerDto::new).orElse(null),
         Optional.ofNullable(order.getDelivery()).map(OrderDeliveryDto::new).orElse(null),
         Optional.ofNullable(order.getSchedule()).map(OrderScheduleDto::new).orElse(null),
         Optional.ofNullable(order.getTakeout()).map(OrderTakeoutDto::new).orElse(null),
         Optional.ofNullable(order.getCommand()).map(CommandDto::new).orElse(null),
         Optional.ofNullable(order.getPayment()).map(PaymentRecordDto::new).orElse(null),
         order.getItems().stream().map(OrderItemDto::new).toList(),
         Optional.ofNullable(order.getBenefits()).map(benefits -> benefits.stream().map(OrderBenefitDto::new).toList()).orElse(List.of()),
         Optional.ofNullable(order.getAdditionalFees()).map(fees -> fees.stream().map(OrderAdditionalFeeDto::new).toList()).orElse(List.of())
         );
    }

    public FullOrderDto withPrinted(boolean printed) {
    return new FullOrderDto(
        id, merchantSequence, modifiedAt, createdAt, preparationStartDateTime,
        type, status, salesChannel, timing, extraInfo,
        printed,                    
        merchantId, total, customer, delivery, schedule,
        takeout, command, payment, items, benefits, additionalFees
    );
}

    public FullOrderDto withStatus(OrderStatus newStatus) {
        return new FullOrderDto(
            id, merchantSequence, modifiedAt, createdAt, preparationStartDateTime,
            type, newStatus,          
            salesChannel, timing, extraInfo, printed,
            merchantId, total, customer, delivery, schedule,
            takeout, command, payment, items, benefits, additionalFees
        );
    }



    public String toComandString() {
        StringBuilder sb = new StringBuilder();
        sb.append("--- ").append(translateType(type)).append(" ---\n");
        sb.append("Pedido: ").append(merchantSequence).append("\n");
        sb.append("Data: ").append(DateUtils.formatDateToBrazilianTime(createdAt)).append("\n");
        sb.append("Tipo: ").append(translateType(type)).append("\n");
        sb.append("Status: ").append(translateStatus(status)).append("\n");
        sb.append("-------------------\n");
        
        if (customer != null) {
            sb.append("Nome: ").append(customer.name()).append("\n");
        }
        if (delivery != null) {
            sb.append("Entrega: ").append(delivery.address().formattedAddress()).append("\n");
        } else if (command != null) {
            sb.append("Mesa: ").append(command.tableIndex() != null ? command.tableIndex() : "-").append("\n");
            sb.append("Comanda: ").append(command.name() != null ? command.name() : "-").append("\n");
        } else if (takeout != null) {
            sb.append("Retirada\n");
        }
        sb.append("-------------------\n");

        java.text.DecimalFormat df = new java.text.DecimalFormat("#,##0.00");
    
        for (OrderItemDto item : items) {
            String itemPrice = (item.totalPrice() == null)
                ? "0,00"
                : df.format(item.totalPrice());
            
            sb.append("(")
              .append(item.quantity())
              .append(") ")
              .append(item.item().name())
              .append("  R$ ")
              .append(itemPrice)
              .append("\n");
            if (item.observations() != null) {
                sb.append(item.observations()).append("\n");
            }
    
            if (item.options() != null && !item.options().isEmpty()) {
                for (OrderItemOptionDto option : item.options()) {
                    String optionPrice = (option.totalPrice() == null)
                        ? "0,00"
                        : df.format(option.totalPrice());

                    sb.append("   - ")
                      .append(option.option().name())
                      .append("  R$ ")
                      .append(optionPrice)
                      .append("\n");
                }
            }
        }
        
        sb.append("-------------------\n");
        sb.append("Total: R$ ").append(total.orderAmount()).append("\n");
        if (extraInfo != null) {
            sb.append("Info extra: ").append(extraInfo).append("\n");
        }


        String printable = sb.toString()
                .replace("Ç", "C")
                .replace("ç", "c")
                .replace("ã", "a")
                .replace("Ã", "A")
                .replace("á", "a")
                .replace("Á", "A");

        System.err.println(printable);
        return printable;
    }


    public static String translateType(OrderType type) {
        if (type == null) return "Desconhecido";
        return switch (type) {
            case DELIVERY -> "Entrega";
            case SCHEDULE -> "Agendado";
            case TAKEOUT -> "Retirada";
            case COMMAND -> "Comanda";
        };
    }
    
    public static String translateStatus(OrderStatus status) {
        if (status == null) return "Desconhecido";
        return switch (status) {
            case CREATED -> "Criado";
            case CONFIRMED -> "Confirmado";
            case PREPARATION_STARTED -> "Em preparo";
            case READY_TO_PICKUP -> "Pronto p/ retirar";
            case DISPATCHED -> "Despachado";
            case COMPLETED -> "Concluído";
            case CANCELED -> "Cancelado";
        };
    }
    
}
