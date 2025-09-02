package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.catalog.domain.entity.Option;

public interface OptionRepository extends JpaRepository<Option, UUID> {

    List<Option> findAllByOptionGroupId(UUID optionGroupId);

    Option findByIdAndOptionGroupId(UUID id, UUID optionGroupId);

}
