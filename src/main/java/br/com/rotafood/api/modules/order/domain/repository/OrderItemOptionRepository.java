package br.com.rotafood.api.modules.order.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.order.domain.entity.OrderItemOption;

import java.util.UUID;

public interface OrderItemOptionRepository extends JpaRepository<OrderItemOption, UUID> {
}
