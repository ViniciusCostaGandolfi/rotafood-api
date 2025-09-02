package br.com.rotafood.api.modules.logistic.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;

public record DistanceInDto(
    UUID id,
    AddressDto origin,
    AddressDto destiny
) { }

