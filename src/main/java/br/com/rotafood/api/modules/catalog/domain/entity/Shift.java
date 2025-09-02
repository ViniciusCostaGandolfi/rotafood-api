package br.com.rotafood.api.modules.catalog.domain.entity;

import java.time.LocalTime;
import java.util.UUID;

import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
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
@Table(name = "shifts")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class Shift {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    private LocalTime startTime;
    private LocalTime endTime;

    private Boolean monday;
    private Boolean tuesday;
    private Boolean wednesday;
    private Boolean thursday;
    private Boolean friday;
    private Boolean saturday;
    private Boolean sunday;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "itemId", referencedColumnName = "id", nullable = true)
    private Item item;

    @ManyToOne(fetch = FetchType.LAZY)    
    @JoinColumn(name = "merchantId", referencedColumnName = "id", nullable = true)
    private Merchant merchant;
}
