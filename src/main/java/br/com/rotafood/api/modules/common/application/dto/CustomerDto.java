package br.com.rotafood.api.modules.common.application.dto;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

import br.com.rotafood.api.modules.common.domain.entity.Customer;

public record CustomerDto(
    UUID id,
    @NotNull
    String name,
    @NotNull
    String phone
) {
    public CustomerDto(Customer customer) {
        this(
            customer.getId(),
            customer.getName(),
            customer.getPhone()
        );
    }
}
