package br.com.rotafood.api.modules.common.application.dto;

import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.common.domain.entity.Customer;

public record FullCustomerDto(
    UUID id,
    String name,
    String phone,
    List<AddressDto> addresses
) {
    public FullCustomerDto(Customer customer) {
        this(
            customer.getId(),
            customer.getName(),
            customer.getPhone(),
            customer.getAddresses()
                .stream()
                .map(ca -> new AddressDto(ca.getAddress()))
                .toList()
        );
    }
}
