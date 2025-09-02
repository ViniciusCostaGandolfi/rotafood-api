package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.catalog.domain.entity.SellingOption;


public interface SellingOptionRepository extends JpaRepository<SellingOption, UUID>  {



}