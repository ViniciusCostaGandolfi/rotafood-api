package br.com.rotafood.api.modules.order.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import br.com.rotafood.api.modules.order.domain.entity.Command;
import br.com.rotafood.api.modules.order.domain.entity.CommandStatus;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface CommandRepository extends JpaRepository<Command, UUID> {
    
    List<Command> findAllByMerchantIdAndStatus(UUID merchantId, CommandStatus status);

    Optional<Command> findByIdAndMerchantId(UUID id, UUID merchantId);

    @Query("""
        SELECT MAX(c.merchantSequence) 
          FROM Command c 
         WHERE c.merchant.id = :merchantId
    """)
    Long findMaxMerchantSequenceByMerchantId(UUID merchantId);


    List<Command> findByCreatedAtBeforeAndStatusNot(Instant cutoff, CommandStatus status);


}
