package br.com.rotafood.api.modules.catalog.domain.entity;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Entity
@Table(name = "packagings")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Packaging {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, length = 64)
    private String name;

    @Column
    private String imagePath;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal lenghtCm;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal widthCm;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal thicknessCm; 

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal volumeMl; 

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "merchantId", nullable = false)
    private Merchant merchant;
}
