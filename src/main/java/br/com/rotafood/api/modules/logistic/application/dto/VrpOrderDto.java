package br.com.rotafood.api.modules.logistic.application.dto;

import java.math.BigDecimal;
import java.util.Date;
import java.util.UUID;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;

public record VrpOrderDto (
    UUID id,
    BigDecimal volumeLiters,
    Date createdAt,
    AddressDto address
) {}
