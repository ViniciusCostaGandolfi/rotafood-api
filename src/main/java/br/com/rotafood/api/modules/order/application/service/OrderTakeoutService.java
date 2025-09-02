package br.com.rotafood.api.modules.order.application.service;

import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.rotafood.api.modules.order.application.dto.OrderTakeoutDto;
import br.com.rotafood.api.modules.order.domain.entity.OrderTakeout;
import br.com.rotafood.api.modules.order.domain.repository.OrderTakeoutRepository;


@Service
public class OrderTakeoutService {

    @Autowired
    private OrderTakeoutRepository orderTakeoutRepository;

    @Transactional
    public OrderTakeout createOrUpdate(OrderTakeoutDto orderTakeoutDto) {

        OrderTakeout takeout = orderTakeoutDto.id() != null
                ? orderTakeoutRepository.findById(orderTakeoutDto.id())
                        .orElseThrow(() -> new EntityNotFoundException("OrderTakeout not found."))
                : new OrderTakeout();

        takeout.setTakeoutDateTime(orderTakeoutDto.takeoutDateTime());
        takeout.setComments(orderTakeoutDto.comments());

        return orderTakeoutRepository.save(takeout);
    }
}
