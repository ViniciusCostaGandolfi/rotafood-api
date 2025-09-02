package br.com.rotafood.api.modules.order.domain.entity;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.catalog.domain.entity.ContextModifier;
import br.com.rotafood.api.modules.catalog.domain.entity.Option;
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

@Table(name = "order_item_options")
@Entity
@AllArgsConstructor
@NoArgsConstructor
@EqualsAndHashCode
@Getter
@Setter
public class OrderItemOption {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column
    private int quantity;

    @Column(precision = 10, scale = 2)
    private BigDecimal totalPrice;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "contextModifierId")
    private ContextModifier contextModifier;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "optionId")
    private Option option;

}
