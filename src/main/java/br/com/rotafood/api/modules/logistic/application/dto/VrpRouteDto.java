package br.com.rotafood.api.modules.logistic.application.dto;

import java.util.List;
import java.util.UUID;

public record VrpRouteDto (
    UUID id,
    List<Integer> sequence,
    List<VrpOrderDto> orders,
    List<CoordinateDto> routeLine,
    double distanceMeters,
    double volumeLiters,
    String linkGoogleMaps
) {}
