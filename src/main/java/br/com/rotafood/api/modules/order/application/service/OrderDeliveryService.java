package br.com.rotafood.api.modules.order.application.service;

import br.com.rotafood.api.modules.common.domain.entity.Address;
import br.com.rotafood.api.modules.common.domain.repository.AddressRepository;
import br.com.rotafood.api.modules.order.application.dto.OrderDeliveryDto;
import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderDelivery;
import br.com.rotafood.api.modules.order.domain.repository.OrderDeliveryRepository;
import br.com.rotafood.api.modules.order.domain.repository.OrderRepository;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class OrderDeliveryService {

    @Autowired
    private OrderDeliveryRepository orderDeliveryRepository;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private AddressRepository addressRepository;

    @Transactional
    public OrderDelivery createOrUpdate(OrderDeliveryDto orderDeliveryDto) {

        OrderDelivery orderDelivery = orderDeliveryDto.id() != null
            ? this.orderDeliveryRepository.findById(orderDeliveryDto.id()).orElseThrow(() -> 
                new EntityNotFoundException("Delivery não encontrado para ID: " + orderDeliveryDto.id()))
            : new OrderDelivery();

        Address address = this.addressRepository.save(new Address(orderDeliveryDto.address()));

        
        orderDelivery.setDeliveryBy(orderDeliveryDto.deliveryBy());
        orderDelivery.setMode(orderDeliveryDto.mode());
        orderDelivery.setDescription(orderDeliveryDto.description());
        orderDelivery.setPickupCode(orderDeliveryDto.pickupCode());
        orderDelivery.setDeliveryDateTime(orderDeliveryDto.deliveryDateTime());
        orderDelivery.setAddress(address);
        orderDeliveryRepository.save(orderDelivery);

        return orderDelivery;
    }




    @Transactional
    public void deleteByOrderId(UUID orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new EntityNotFoundException("Order not found."));

        if (order.getDelivery() != null) {
            orderDeliveryRepository.delete(order.getDelivery());
            order.setDelivery(null);
            orderRepository.save(order);
        }
    }

    public OrderDelivery getByOrderId(UUID orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new EntityNotFoundException("Order not found."));
        return order.getDelivery();
    }
}
