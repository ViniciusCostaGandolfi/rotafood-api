package br.com.rotafood.api.modules.order.application.service;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderStatus;
import br.com.rotafood.api.modules.order.domain.entity.OrderTiming;
import br.com.rotafood.api.modules.order.domain.repository.OrderRepository;

@Component
public class OrderStatusSchedulerService {

    @Autowired
    private OrderRepository orderRepository;

    @Scheduled(fixedDelay = 60000000)
    public void updateOrdersStatus() {
        orderRepository.count();
        Instant cutoffTime = Instant.now()
                .minus(2, ChronoUnit.HOURS)
                .minus(30, ChronoUnit.MINUTES);

        List<Order> orders = orderRepository.findByPreparationStartDateTimeBeforeAndStatusNotAndTiming(
                cutoffTime, 
                OrderStatus.COMPLETED,
                OrderTiming.IMMEDIATE);

        orders.forEach(order -> {
            order.setStatus(OrderStatus.COMPLETED);
            orderRepository.save(order);
        });
    }
}
