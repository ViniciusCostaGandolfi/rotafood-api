package br.com.rotafood.api.modules.merchant.domain.entity;

import java.math.BigDecimal;
import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "merchant_logistic_settings")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class MerchantLogisticSetting {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(precision = 10, scale = 2, nullable = false)
    private BigDecimal minDeliveryFee;

    @Column(precision = 10, scale = 4, nullable = false)
    private BigDecimal deliveryFeePerKm;

    @Column(precision = 10, scale = 2, nullable = false)
    private BigDecimal maxDeliveryRadiusKm;

    @Column(precision = 10, scale = 2)
    private BigDecimal freeDeliveryRadiusKm;

    @Column(precision = 9, scale = 6)
    private BigDecimal latitude;

    @Column(precision = 9, scale = 6)
    private BigDecimal longitude;

}
