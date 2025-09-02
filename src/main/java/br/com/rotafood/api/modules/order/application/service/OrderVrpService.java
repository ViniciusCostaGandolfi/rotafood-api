package br.com.rotafood.api.modules.order.application.service;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.logistic.application.dto.VrpInDto;
import br.com.rotafood.api.modules.logistic.application.dto.VrpOrderDto;
import br.com.rotafood.api.modules.logistic.application.dto.VrpOriginDto;
import br.com.rotafood.api.modules.logistic.application.dto.VrpOutDto;
import br.com.rotafood.api.modules.logistic.application.service.LogisticService;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderStatus;
import br.com.rotafood.api.modules.order.domain.entity.OrderType;
import br.com.rotafood.api.modules.order.domain.repository.OrderRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;

@Service
@Transactional
public class OrderVrpService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private MerchantRepository merchantRepository;

    @Autowired
    private LogisticService logisticService;


    public VrpOutDto generateDeliveryRoutes(UUID merchantId) {
        Merchant merchant = merchantRepository.findById(merchantId)
                .orElseThrow(() -> new RuntimeException("Merchant not found."));

        Instant end = Instant.now();
        Instant start = end.minus(12, ChronoUnit.HOURS);
        List<Order> orders = orderRepository.findAllByFilters(
            merchantId, 
            List.of(OrderType.DELIVERY),
            List.of(OrderStatus.READY_TO_PICKUP), 
            start, 
            null, 
            Pageable.unpaged()).toList();



        if (orders.isEmpty()) {
            throw new RuntimeException("No DELIVERY orders with READY_TO_PICKUP status found.");
        }

            VrpOriginDto origin = new VrpOriginDto(merchant.getId(),  new AddressDto(merchant.getAddress()));

        List<VrpOrderDto> vrpOrders = orders.stream()
                .map(this::mapToVrpOrderDto)
                .collect(Collectors.toList());

        VrpInDto vrpIn = new VrpInDto(
                UUID.randomUUID(),    
                origin,                
                vrpOrders,             
                new BigDecimal(45),                 
                new Date() 
        );

        VrpOutDto routesResult = logisticService.logisticRoutesForOrders(vrpIn);
        return routesResult;
    }


    private VrpOrderDto mapToVrpOrderDto(Order order) {
        if (order.getDelivery() == null || order.getDelivery().getAddress() == null) {
            throw new RuntimeException("Order does not have a delivery address: " + order.getId());
        }

        double volume = 10;

        return new VrpOrderDto(
                order.getId(),
                new BigDecimal(volume),
                order.getCreatedAt() != null ? Date.from(order.getCreatedAt()) : new Date(),
                new AddressDto(order.getDelivery().getAddress())
        );
    }
}
