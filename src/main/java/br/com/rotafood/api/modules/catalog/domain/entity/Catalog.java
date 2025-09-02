package br.com.rotafood.api.modules.catalog.domain.entity;

import java.util.Date;
import java.util.UUID;

import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
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
import lombok.Setter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "catalogs")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Catalog {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column
    private Date modifiedAt;

    @Column
    @Enumerated(EnumType.STRING)
    private AvailabilityStatus status;

    @Column
    @Enumerated(EnumType.STRING)
    private CatalogContext catalogContext;
 
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "merchantId") 
    private Merchant merchant;

    @Column(nullable = true)
    private UUID iFoodCatalogId;
}
