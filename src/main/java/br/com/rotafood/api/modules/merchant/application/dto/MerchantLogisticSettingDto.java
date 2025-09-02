package br.com.rotafood.api.modules.merchant.application.dto;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.merchant.domain.entity.MerchantLogisticSetting;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;


public record MerchantLogisticSettingDto(
    UUID id,
    @NotNull
    @Min(0)
    BigDecimal minDeliveryFee,
    @NotNull
    @Min(0)
    BigDecimal deliveryFeePerKm,
    @NotNull
    @Min(0)
    BigDecimal maxDeliveryRadiusKm,
    @NotNull
    @Min(0)
    BigDecimal freeDeliveryRadiusKm,
    BigDecimal latitude,
    BigDecimal longitude

) {

    public MerchantLogisticSettingDto(MerchantLogisticSetting logisticSetting) {
        this(
            logisticSetting.getId(), 
            logisticSetting.getMinDeliveryFee(), 
            logisticSetting.getDeliveryFeePerKm(), 
            logisticSetting.getMaxDeliveryRadiusKm(),
            logisticSetting.getFreeDeliveryRadiusKm(),
            logisticSetting.getLatitude(),
            logisticSetting.getLongitude()
            );
    }
    
}
