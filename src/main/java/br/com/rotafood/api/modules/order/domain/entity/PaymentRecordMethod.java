package br.com.rotafood.api.modules.order.domain.entity;

import java.math.BigDecimal;
import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
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
@Table(name = "payment_record_methods")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class PaymentRecordMethod {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(length = 1024)
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(length = 20, nullable = false)
    private PaymentRecordMethodType method;

    @Column(nullable = false)
    private boolean paid;

    @Enumerated(EnumType.STRING)
    @Column(length = 10, nullable = false)
    private PaymentRecordType type;

    @Column(precision = 10, scale = 2, nullable = false)
    private BigDecimal value;

    @Column(precision = 10, scale = 2)
    private BigDecimal changeFor;

}

