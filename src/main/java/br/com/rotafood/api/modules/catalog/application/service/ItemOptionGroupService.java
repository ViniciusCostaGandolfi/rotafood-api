package br.com.rotafood.api.modules.catalog.application.service;

import br.com.rotafood.api.modules.catalog.application.dto.FullItemOptionGroupDto;
import br.com.rotafood.api.modules.catalog.domain.entity.Item;
import br.com.rotafood.api.modules.catalog.domain.entity.ItemOptionGroup;
import br.com.rotafood.api.modules.merchant.domain.repository.ItemOptionGroupRepository;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class ItemOptionGroupService {

    @Autowired
    private ItemOptionGroupRepository itemOptionGroupRepository;

    @Autowired
    private OptionGroupService optionGroupService;

    @Transactional
    public List<ItemOptionGroup> createOrUpdateAll(List<FullItemOptionGroupDto> dtos, Item item, UUID merchantId, boolean updateOptionGroups) {
        if (dtos == null || dtos.isEmpty()) {
            new ArrayList<>(item.getItemOptionGroups()).forEach(item::removeItemOptionGroup);
            return List.of();
        }

        List<UUID> incomingIds = dtos.stream()
                .map(FullItemOptionGroupDto::id)
                .filter(Objects::nonNull)
                .toList();

        List<ItemOptionGroup> toRemove = item.getItemOptionGroups().stream()
                .filter(iog -> iog.getId() != null && !incomingIds.contains(iog.getId()))
                .toList();

        toRemove.forEach(item::removeItemOptionGroup);

        dtos.forEach(dto -> {
            ItemOptionGroup group = dto.id() != null ? 
                itemOptionGroupRepository.findById(dto.id()).orElseThrow(() -> new EntityNotFoundException("Grupo não encontrado: " + dto.id()))
                : new ItemOptionGroup();
                
            group.setOptionGroup(optionGroupService.getByIdAndMerchantId(dto.optionGroup().id(), merchantId));
            group.setItem(item);
            group.setIndex(dto.index());
            group.setMin(dto.min());
            group.setMax(dto.max());

            if (!item.getItemOptionGroups().contains(group)) {
                item.addItemOptionGroup(group);
            }

            this.itemOptionGroupRepository.save(group);




        });

        return item.getItemOptionGroups();
    }

}
