package br.com.rotafood.api.modules.order.application.service;

import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.rotafood.api.modules.order.application.dto.OrderScheduleDto;
import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderSchedule;
import br.com.rotafood.api.modules.order.domain.repository.OrderRepository;
import br.com.rotafood.api.modules.order.domain.repository.OrderScheduleRepository;

import java.util.UUID;

@Service
public class OrderScheduleService {

    @Autowired
    private OrderScheduleRepository orderScheduleRepository;

    @Autowired
    private OrderRepository orderRepository;

    @Transactional
    public OrderSchedule createOrUpdate(OrderScheduleDto orderScheduleDto) {
        OrderSchedule schedule = orderScheduleDto.id() != null
                ? orderScheduleRepository.findById(orderScheduleDto.id())
                        .orElseThrow(() -> new EntityNotFoundException("OrderSchedule not found."))
                : new OrderSchedule();

        schedule.setDeliveryDateTimeStart(orderScheduleDto.deliveryDateTimeStart());
        schedule.setDeliveryDateTimeEnd(orderScheduleDto.deliveryDateTimeEnd());


        return orderScheduleRepository.save(schedule);
    }

    @Transactional
    public void deleteByOrderId(UUID orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new EntityNotFoundException("Order not found."));

        if (order.getSchedule() != null) {
            orderScheduleRepository.delete(order.getSchedule());
            order.setSchedule(null);
            orderRepository.save(order);
        }
    }

    public OrderSchedule getByOrderId(UUID orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new EntityNotFoundException("Order not found."));
        return order.getSchedule();
    }
}
