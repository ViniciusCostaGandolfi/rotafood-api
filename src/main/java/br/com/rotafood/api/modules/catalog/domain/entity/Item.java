package br.com.rotafood.api.modules.catalog.domain.entity;

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
import jakarta.persistence.OneToMany;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;


@Entity
@Table(name = "items")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Item {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column
    @Enumerated(EnumType.STRING)
    private AvailabilityStatus status;
    
    @Column
    private Integer index;

    @Column
    @Enumerated(EnumType.STRING)
    private TemplateType type;

    @Column(nullable = true)
    private UUID iFoodItemId;
    
    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "merchantId", nullable = false)
    private Merchant merchant;

    @OneToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "productId")    
    private Product product;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "categoryId")
    private Category category;

    @OneToMany(mappedBy = "item", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ContextModifier> contextModifiers = new ArrayList<>();

    @OneToMany(mappedBy = "item", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Shift> shifts = new ArrayList<>();

    @OneToMany(mappedBy = "item", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.EAGER)
    private List<ItemOptionGroup> itemOptionGroups = new ArrayList<>();
    public void addItemOptionGroup(ItemOptionGroup itemOptionGroup) {
        this.itemOptionGroups.add(itemOptionGroup);
        itemOptionGroup.setItem(this);
    }

    public void removeItemOptionGroup(ItemOptionGroup itemOptionGroup) {
        this.itemOptionGroups.remove(itemOptionGroup);
        itemOptionGroup.setItem(null);
    }
    

    public void addContextModifier(ContextModifier modifier) {
        this.contextModifiers.add(modifier);
        modifier.setItem(this);
    }

    public void removeContextModifier(ContextModifier modifier) {
        this.contextModifiers.remove(modifier);
        modifier.setItem(null);
    }

    public void addShift(Shift shift) {
        this.shifts.add(shift);
        shift.setItem(this);
    }

    public void removeShift(Shift shift) {
        this.shifts.remove(shift);
        shift.setItem(null);
    }

}
