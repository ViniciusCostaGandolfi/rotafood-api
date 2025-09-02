package br.com.rotafood.api.modules.order.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.order.domain.entity.OrderTotal;

import java.util.UUID;

public interface OrderTotalRepository extends JpaRepository<OrderTotal, UUID> {
}
