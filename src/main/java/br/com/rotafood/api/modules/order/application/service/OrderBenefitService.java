package br.com.rotafood.api.modules.order.application.service;

import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.rotafood.api.modules.order.application.dto.OrderBenefitDto;
import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderBenefit;
import br.com.rotafood.api.modules.order.domain.repository.OrderBenefitRepository;

import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Service
public class OrderBenefitService {

    @Autowired
    private OrderBenefitRepository orderBenefitRepository;

    @Transactional
    public OrderBenefit createOrUpdate(OrderBenefitDto benefitDto, Order order) {
        OrderBenefit benefit = benefitDto.id() != null
                ? orderBenefitRepository.findById(benefitDto.id())
                        .orElseThrow(() -> new EntityNotFoundException("Benefício não encontrado."))
                : new OrderBenefit();

        benefit.setValue(benefitDto.value());
        benefit.setDescription(benefitDto.description());
        benefit.setTarget(benefitDto.target());

        order.getBenefits().add(benefit);

        return orderBenefitRepository.save(benefit);
    }

    @Transactional
    public void synchronizeBenefits(List<OrderBenefitDto> benefitDtos, Order order) {
        List<UUID> newBenefitIds = benefitDtos.stream()
                .map(OrderBenefitDto::id)
                .filter(Objects::nonNull)
                .toList();

        order.getBenefits().removeIf(existingBenefit ->
                existingBenefit.getId() != null && !newBenefitIds.contains(existingBenefit.getId()));

        benefitDtos.forEach(benefitDto -> this.createOrUpdate(benefitDto, order));
    }
}
