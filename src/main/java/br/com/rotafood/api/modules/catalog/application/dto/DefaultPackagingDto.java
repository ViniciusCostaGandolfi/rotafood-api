package br.com.rotafood.api.modules.catalog.application.dto;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.DefaultPackaging;

public record DefaultPackagingDto(
    UUID id,
    String name,
    String imagePath,
    String iFoodImagePath,
    BigDecimal lenghtCm,
    BigDecimal widthCm,
    BigDecimal thicknessCm,
    BigDecimal volumeMl
) {
    public DefaultPackagingDto(DefaultPackaging packaging) {
        this(
            packaging.getId(), 
            packaging.getName(), 
            packaging.getImagePath(), 
            packaging.getIFoodImagePath(), 
            packaging.getLenghtCm(), 
            packaging.getWidthCm(), 
            packaging.getThicknessCm(), 
            packaging.getVolumeMl());
    }
}