package br.com.rotafood.api.modules.order.application.dto;

import java.util.Date;
import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.OrderSchedule;

public record OrderScheduleDto(
    UUID id,
    Date deliveryDateTimeStart,
    Date deliveryDateTimeEnd
) {
    public OrderScheduleDto(OrderSchedule schedule) {
        this(
            schedule.getId(),
            schedule.getDeliveryDateTimeStart(),
            schedule.getDeliveryDateTimeEnd()
        );
    }

}

