package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUser;

public interface MerchantUserRepository extends JpaRepository<MerchantUser, UUID> {

    boolean existsByEmail(String email);

    MerchantUser findByEmail(String email);

    Optional<MerchantUser>  findByIdAndMerchantId(UUID merchantId, UUID merchantUserId);

    List<MerchantUser> findByMerchantId(UUID merchantId);

}