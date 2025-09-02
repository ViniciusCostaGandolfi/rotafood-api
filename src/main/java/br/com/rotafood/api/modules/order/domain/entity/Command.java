package br.com.rotafood.api.modules.order.domain.entity;


import java.time.Instant;
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
@Table(name = "commands")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Command {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private Integer merchantSequence;

    @Column()
    private Integer tableIndex;

    @Column()
    private String name;

    @OneToMany(mappedBy = "command", cascade = CascadeType.ALL)
    private List<Order> orders;

    @Enumerated(EnumType.STRING)
    private CommandStatus status;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "merchantId")
    private Merchant merchant;


    @Column(nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    
}
