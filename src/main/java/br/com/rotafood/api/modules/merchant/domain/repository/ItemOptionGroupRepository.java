package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.catalog.domain.entity.ItemOptionGroup;


public interface ItemOptionGroupRepository extends JpaRepository<ItemOptionGroup, UUID> {

    ItemOptionGroup findByIdAndOptionGroupId(UUID id, UUID optionGroupId);

    ItemOptionGroup findByItemIdAndOptionGroupId(UUID itemId, UUID optionGroupId);

    

    List<ItemOptionGroup> findAllByItemId(UUID itemId);

}
