package br.com.rotafood.api.modules.common.application.dto;

import br.com.rotafood.api.modules.common.domain.entity.Address;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;
import java.util.UUID;


public record AddressDto(
    UUID id,
    @NotBlank String country,
    @NotBlank String state,
    @NotBlank String city,
    @NotNull String neighborhood,
    @NotBlank @Size(min = 8, max = 9, message = "O CEP deve ter entre 8 e 9 caracteres") 
    String postalCode,
    @NotBlank String streetName,
    @NotNull String streetNumber,
    @NotNull String formattedAddress,
    String complement,
    @NotNull BigDecimal latitude,
    @NotNull BigDecimal longitude
) {
    public AddressDto(Address address) {
        this(
            address.getId(),
            address.getCountry(),
            address.getState(),
            address.getCity(),
            address.getNeighborhood(),
            address.getPostalCode(),
            address.getStreetName(),
            address.getStreetNumber(),
            address.getFormattedAddress(),
            address.getComplement(),
            address.getLatitude(),
            address.getLongitude()
        );
    }
}