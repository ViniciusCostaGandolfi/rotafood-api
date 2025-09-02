package br.com.rotafood.api.modules.order.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.order.domain.entity.OrderSchedule;

import java.util.UUID;

public interface OrderScheduleRepository extends JpaRepository<OrderSchedule, UUID> {
}
