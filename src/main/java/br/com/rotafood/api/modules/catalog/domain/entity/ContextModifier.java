package br.com.rotafood.api.modules.catalog.domain.entity;


import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

import java.util.UUID;


@Entity
@Table(name = "context_modifiers")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class ContextModifier {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @Enumerated(EnumType.STRING)
    private AvailabilityStatus status;
    
    @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "priceId")
    private Price price;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "itemId", nullable = true)
    private Item item;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "optionId", nullable = true)
    private Option option;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "parentOptionId", referencedColumnName = "id", nullable = true)
    private Option parentOptionModifier;


    @Enumerated(EnumType.STRING)
    private CatalogContext catalogContext;
}
