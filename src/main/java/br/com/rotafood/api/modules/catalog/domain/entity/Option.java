package br.com.rotafood.api.modules.catalog.domain.entity;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

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

@Entity
@Table(name = "options")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Option {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    private AvailabilityStatus status;

    @Column
    private Integer index;

    @OneToMany(mappedBy = "option", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ContextModifier> contextModifiers = new ArrayList<>();

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "optionGroupId")  
    private OptionGroup optionGroup;
    
    @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "productId")    
    private Product product;

    @Column(columnDefinition = "integer[]")
    private List<Integer> fractions;

    @Column(nullable = true)
    private UUID iFoodOptionId;

    public void addContextModifier(ContextModifier modifier) {
        this.contextModifiers.add(modifier);
        modifier.setOption(this);
    }

    public void removeContextModifier(ContextModifier modifier) {
        this.contextModifiers.remove(modifier);
        modifier.setOption(null);
    }

}