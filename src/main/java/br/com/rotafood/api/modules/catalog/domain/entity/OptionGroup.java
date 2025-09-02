package br.com.rotafood.api.modules.catalog.domain.entity;

import java.util.ArrayList;
import java.util.List;
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
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "option_groups")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class OptionGroup {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    private String name;

    @Column
    @Enumerated(value = EnumType.STRING)
    private OptionGroupType optionGroupType;
    
    @Column
    @Enumerated(value = EnumType.STRING)
    private AvailabilityStatus status;
    
    @OneToMany(mappedBy = "optionGroup", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    private List<Option> options = new ArrayList<>();
    
    @ManyToOne(fetch = FetchType.LAZY)     
    @JoinColumn(name = "merchantId")
    private Merchant merchant;

    @Column(nullable = true)
    private UUID iFoodOptionGroupId;

    public void addOption(Option option) {
        this.options.add(option);
        option.setOptionGroup(this);
    }

    public void removeOption(Option option) {
        this.options.remove(option);
        option.setOptionGroup(null);
    }
}