package br.com.rotafood.api.modules.order.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.order.domain.entity.PaymentRecord;

import java.util.UUID;

public interface PaymentRecordRepository extends JpaRepository<PaymentRecord, UUID> {
}
