package br.com.rotafood.api.modules.catalog.domain.entity;
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
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "item_option_group")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class ItemOptionGroup {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "itemId")
    private Item item;

    @Column
    private Integer min;

    @Column 
    private Integer max;
    
    @Column
    private Integer index;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "optionGroupId")
    private OptionGroup optionGroup;

}