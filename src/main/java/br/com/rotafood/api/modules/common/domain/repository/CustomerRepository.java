package br.com.rotafood.api.modules.common.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.common.domain.entity.Customer;

import java.util.Optional;
import java.util.UUID;

public interface CustomerRepository extends JpaRepository<Customer, UUID> {
    Optional<Customer> findByPhone(String phone);
}
