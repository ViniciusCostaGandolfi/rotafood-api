package br.com.rotafood.api.modules.logistic.application.dto;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.UUID;


public record VrpInDto (
    UUID id,
    VrpOriginDto origin,
    List<VrpOrderDto> orders, 
    BigDecimal maxRouteVolume,
    Date createdAt
) {
    
}
