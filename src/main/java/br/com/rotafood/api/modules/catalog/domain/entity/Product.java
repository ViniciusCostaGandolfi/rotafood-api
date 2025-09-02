package br.com.rotafood.api.modules.catalog.domain.entity;

import java.util.UUID;

import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import jakarta.persistence.CascadeType;
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
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "products")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, length = 128)
    private String name;

    @Column(nullable = true, length = 1024)
    private String description;

    @Column(length = 256)
    private String ean;

    @Column(length = 512)
    private String additionalInformation;

    @Column(nullable = false)
    @Enumerated(value = EnumType.STRING)
    private Serving serving = Serving.NOT_APPLICABLE; 
    
    private String imagePath;
    
    @Column
    @Enumerated(value = EnumType.STRING)
    private PackagingType packagingType = PackagingType.NOT_APPLICABLE;

    @Column
    private Integer quantity;

    @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "productPackagingId")
    private ProductPackaging productPackaging;


    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "merchantId", nullable = false)
    private Merchant merchant;
}