package br.com.rotafood.api.modules.order.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.order.domain.entity.PaymentRecordMethod;

import java.util.UUID;

public interface PaymentRecordMethodRepository extends JpaRepository<PaymentRecordMethod, UUID> {
}
