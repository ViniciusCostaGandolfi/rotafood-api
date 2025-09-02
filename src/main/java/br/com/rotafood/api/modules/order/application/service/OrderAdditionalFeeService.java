package br.com.rotafood.api.modules.order.application.service;

import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.rotafood.api.modules.order.application.dto.OrderAdditionalFeeDto;
import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderAdditionalFee;
import br.com.rotafood.api.modules.order.domain.repository.OrderAdditionalFeeRepository;

import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Service
public class OrderAdditionalFeeService {

    @Autowired
    private OrderAdditionalFeeRepository orderAdditionalFeeRepository;

    @Transactional
    public OrderAdditionalFee createOrUpdate(OrderAdditionalFeeDto additionalFeeDto, Order order) {
        OrderAdditionalFee additionalFee = additionalFeeDto.id() != null
                ? orderAdditionalFeeRepository.findById(additionalFeeDto.id())
                        .orElseThrow(() -> new EntityNotFoundException("Adicional não encontrado."))
                : new OrderAdditionalFee();

        additionalFee.setDescription(additionalFeeDto.description());
        additionalFee.setValue(additionalFeeDto.value());

        order.getAdditionalFees().add(additionalFee);

        return orderAdditionalFeeRepository.save(additionalFee);
    }

    @Transactional
    public void synchronizeAdditionalFees(List<OrderAdditionalFeeDto> additionalFeeDtos, Order order) {
        List<UUID> newAdditionalFeeIds = additionalFeeDtos.stream()
                .map(OrderAdditionalFeeDto::id)
                .filter(Objects::nonNull)
                .toList();

        order.getAdditionalFees().removeIf(existingFee ->
                existingFee.getId() != null && !newAdditionalFeeIds.contains(existingFee.getId()));

        additionalFeeDtos.forEach(feeDto -> this.createOrUpdate(feeDto, order));
    }
}
