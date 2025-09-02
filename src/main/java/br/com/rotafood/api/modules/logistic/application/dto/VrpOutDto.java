package br.com.rotafood.api.modules.logistic.application.dto;

import java.util.Date;
import java.util.List;
import java.util.UUID;

public record VrpOutDto (
    UUID id,
    VrpOriginDto origin,
    List<VrpRouteDto> routes, 
    float maxRouteVolume,
    Date createAt,
    double timeToSolveMs
) {
    
}
