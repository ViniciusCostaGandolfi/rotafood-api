package br.com.rotafood.api.modules.merchant.domain.entity;

import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.Shift;
import br.com.rotafood.api.modules.common.domain.entity.Address;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToMany;
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
@Table(name = "merchants")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Merchant {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(length = 64)
    private String name;
    
    @Column
    private String onlineName;

    @Column(length = 256)
    private String description;

    @Enumerated(value = EnumType.STRING)
    private DocumentType documentType;

    @Column(length = 16)
    private String document;

    @Column
    private String phone;

    @Column(nullable = false)
    private String ownerEmail;


    @Column
    private String imagePath;

    @Enumerated(value = EnumType.STRING)
    private MerchantType merchantType;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(nullable = false)
    private Instant createdAt;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(nullable = false)
    private Instant lastOpenedUtc;

    @Column
    private String stripeCustomerId;

    @Column
    private String stripeSubscriptionId;

    @Column
    private String stripeSessionId;

    @Column
    private Boolean isSubscriptionActive;

    @OneToOne
    @JoinColumn(name = "addressId")
    private Address address;

    @OneToOne(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "merchantLogisticSettingId")
    private MerchantLogisticSetting logisticSetting;

    @OneToOne(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "merchantOrderEstimateId")
    private MerchantOrderEstimate orderEstimate;

    @OneToMany(mappedBy = "merchant", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Shift> openingHours = new ArrayList<>();

    public void addShift(Shift shift) {
        this.openingHours.add(shift);
        shift.setMerchant(this);
    }

    public void removeShift(Shift shift) {
        this.openingHours.remove(shift);
        shift.setMerchant(null);
    }
}
