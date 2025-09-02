package br.com.rotafood.api.modules.merchant.domain.repository;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import jakarta.transaction.Transactional;

public interface MerchantRepository extends JpaRepository<Merchant, UUID> {
    boolean existsByOnlineName(String existsByOnlineName);

    Optional<Merchant> findByOnlineName(String onlineName);

    @Modifying
    @Transactional
    @Query("UPDATE Merchant m SET m.lastOpenedUtc = :lastOpenedUtc WHERE m.id = :merchantId")
    void updateLastOpenedUtc(UUID merchantId, Instant lastOpenedUtc);
}
