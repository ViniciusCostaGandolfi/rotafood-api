package br.com.rotafood.api.modules.order.domain.entity;

import java.math.BigDecimal;
import java.util.Date;
import java.util.UUID;

import br.com.rotafood.api.modules.common.domain.entity.Address;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import jakarta.persistence.Temporal;
import jakarta.persistence.TemporalType;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "order_deliveries")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class OrderDelivery {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Enumerated(EnumType.STRING)
    @Column(length = 20, nullable = false)
    private OrderDeliveryMode mode;

    @Enumerated(EnumType.STRING)
    @Column(length = 20, nullable = false)
    private OrderDeliveryBy deliveryBy;

    @Column(length = 20)
    private String description;

    @Column(length = 256)
    private String pickupCode;

    @Temporal(TemporalType.TIMESTAMP)
    private Date deliveryDateTime;

    @Column()
    private BigDecimal volumeMl;

    @OneToOne
    @JoinColumn(name = "addressId") 
    private Address address;

}
