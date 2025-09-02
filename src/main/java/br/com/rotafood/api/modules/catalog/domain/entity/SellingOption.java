package br.com.rotafood.api.modules.catalog.domain.entity;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

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
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "selling_options")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class SellingOption {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private BigDecimal minimum;

    @Column(nullable = false)
    private BigDecimal incremental;

    @Column(nullable = false, columnDefinition = "text[]")
    private List<String> availableUnits;

    @Column(nullable = false)
    private BigDecimal averageUnit;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "productId")
    private Product product;
}
