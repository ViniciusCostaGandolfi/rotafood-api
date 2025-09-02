package br.com.rotafood.api.modules.order.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.order.domain.entity.OrderBenefit;

import java.util.UUID;

public interface OrderBenefitRepository extends JpaRepository<OrderBenefit, UUID> {
}
