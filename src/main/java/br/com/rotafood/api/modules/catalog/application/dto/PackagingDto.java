package br.com.rotafood.api.modules.catalog.application.dto;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.Packaging;

public record PackagingDto(
    UUID id,
    String name,
    String imagePath,
    BigDecimal lenghtCm,
    BigDecimal widthCm,
    BigDecimal thicknessCm,
    BigDecimal volumeMl
) {
    public PackagingDto(Packaging packaging) {
        this(
            packaging.getId(), 
            packaging.getName(), 
            packaging.getImagePath(), 
            packaging.getLenghtCm(), 
            packaging.getWidthCm(), 
            packaging.getThicknessCm(), 
            packaging.getVolumeMl());    
        }
}