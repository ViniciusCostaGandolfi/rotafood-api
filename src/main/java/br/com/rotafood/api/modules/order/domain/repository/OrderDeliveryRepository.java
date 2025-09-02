package br.com.rotafood.api.modules.order.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.order.domain.entity.OrderDelivery;

import java.util.UUID;

public interface OrderDeliveryRepository extends JpaRepository<OrderDelivery, UUID> {
}
