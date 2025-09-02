package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.merchant.domain.entity.MerchantLogisticSetting;

public interface MerchantLogisticSettingRepository extends JpaRepository<MerchantLogisticSetting, UUID> {

}
 