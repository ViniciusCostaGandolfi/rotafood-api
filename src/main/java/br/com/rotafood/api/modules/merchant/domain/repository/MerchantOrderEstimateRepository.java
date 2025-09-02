package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.merchant.domain.entity.MerchantOrderEstimate;



public interface MerchantOrderEstimateRepository extends JpaRepository<MerchantOrderEstimate, UUID> {


}
 