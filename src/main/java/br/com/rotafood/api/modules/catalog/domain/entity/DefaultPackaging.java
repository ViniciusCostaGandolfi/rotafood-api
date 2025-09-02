package br.com.rotafood.api.modules.catalog.domain.entity;

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
import lombok.NoArgsConstructor;
import lombok.Setter;


@Entity
@Table(name = "default_packagings")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class DefaultPackaging {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, length = 64)
    private String name;

    @Column
    private String imagePath;

    @Column
    private String iFoodImagePath;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal lenghtCm;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal widthCm;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal thicknessCm; 

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal volumeMl; 
}
