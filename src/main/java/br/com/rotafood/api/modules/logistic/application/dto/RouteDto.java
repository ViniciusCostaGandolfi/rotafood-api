package br.com.rotafood.api.modules.logistic.application.dto;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import jakarta.validation.constraints.NotNull;

public record RouteDto(
    UUID id,
    @NotNull
    AddressDto origin,
    @NotNull
    AddressDto destiny,
    @NotNull
    BigDecimal distanceMeters,
    @NotNull
    BigDecimal deliveryFee,
    @NotNull
    List<CoordinateDto> routeLine
) { }
