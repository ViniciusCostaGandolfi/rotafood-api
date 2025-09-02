package br.com.rotafood.api.modules.logistic.application.dto;

import java.math.BigDecimal;

public record CoordinateDto (
    BigDecimal lat,
    BigDecimal lng
) {
    
}
