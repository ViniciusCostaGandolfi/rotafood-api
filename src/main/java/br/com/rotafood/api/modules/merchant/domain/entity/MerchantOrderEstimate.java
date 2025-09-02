package br.com.rotafood.api.modules.merchant.domain.entity;

import java.util.UUID;
import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "merchant_order_estimates")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class MerchantOrderEstimate {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private Integer pickupMinMinutes;

    @Column(nullable = false)
    private Integer pickupMaxMinutes;

    @Column(nullable = false)
    private Integer deliveryMinMinutes;

    @Column(nullable = false)
    private Integer deliveryMaxMinutes;

}
