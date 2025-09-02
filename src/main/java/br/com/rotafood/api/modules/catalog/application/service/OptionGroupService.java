package br.com.rotafood.api.modules.catalog.application.service;

import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.rotafood.api.modules.catalog.application.dto.OptionDto;
import br.com.rotafood.api.modules.catalog.application.dto.OptionGroupDto;
import br.com.rotafood.api.modules.catalog.application.dto.SortRequestDto;
import br.com.rotafood.api.modules.catalog.domain.entity.Option;
import br.com.rotafood.api.modules.catalog.domain.entity.OptionGroup;
import br.com.rotafood.api.modules.catalog.domain.entity.OptionGroupType;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.OptionGroupRepository;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;

@Service
public class OptionGroupService {

    @Autowired
    private OptionGroupRepository optionGroupRepository;

    @Autowired
    private MerchantRepository merchantRepository;

    @Autowired
    private OptionService optionService;

    @Transactional
    public OptionGroup getByIdAndMerchantId(UUID optionGroupId, UUID merchantId) {
        return optionGroupRepository.findById(optionGroupId)
            .filter(optionGroup -> optionGroup.getMerchant().getId().equals(merchantId))
            .orElseThrow(() -> new IllegalArgumentException("OptionGroup não encontrado ou não pertence ao Merchant."));
    }

    @Transactional
    public OptionGroup updateOrCreate(OptionGroupDto optionGroupDto, UUID merchantId) {
        Merchant merchant = merchantRepository.findById(merchantId)
            .orElseThrow(() -> new IllegalArgumentException("Merchant não encontrado."));

        OptionGroup optionGroup = optionGroupDto.id() != null
            ? optionGroupRepository.findById(optionGroupDto.id())
                .orElseThrow(() -> new IllegalArgumentException("OptionGroup não encontrado."))
            : new OptionGroup();

        optionGroup.setName(optionGroupDto.name());

        optionGroup.setStatus(optionGroupDto.status());

        optionGroup.setOptionGroupType(optionGroupDto.optionGroupType());

        optionGroup.setMerchant(merchant);

        optionGroupRepository.save(optionGroup);

        updateOptions(optionGroup, optionGroupDto.options());

        return optionGroup;
    }

    private void updateOptions(OptionGroup optionGroup, List<OptionDto> optionDtos) {
    
        List<UUID> incomingOptionIds = optionDtos.stream()
            .map(OptionDto::id)
            .filter(Objects::nonNull)
            .toList();

        List<Option> optionsToRemove = optionGroup.getOptions().stream()
                .filter(option -> !incomingOptionIds.contains(option.getId()))
                .toList();

        optionsToRemove.forEach(optionGroup::removeOption);

        optionDtos.forEach(optionDto -> {
            optionService.updateOrCreate(optionDto, optionGroup);
        });
    }
    

    @Transactional
    public void deleteByIdAndMerchantId(UUID optionGroupId, UUID merchantId) {
        var optionGroup = optionGroupRepository.findById(optionGroupId)
            .orElseThrow(() -> new IllegalArgumentException("OptionGroup não encontrado."));

        if (!optionGroup.getMerchant().getId().equals(merchantId)) {
            throw new IllegalArgumentException("OptionGroup não pertence ao Merchant informado.");
        }

        optionGroupRepository.delete(optionGroup);
    }


    public List<OptionGroup> getAllByMerchantId(UUID merchantId){
        return this.optionGroupRepository.findAllByMerchantId(merchantId);
    }

    public List<OptionGroup> getAllByMerchantIdAndOptionGroupType(UUID merchantId, OptionGroupType optionGroupType) {
        return this.optionGroupRepository.findAllByMerchantIdAndOptionGroupType(merchantId, optionGroupType);
    }

    @Transactional
    public OptionGroup sortOptions(UUID merchantId, UUID optionGroupId, List<SortRequestDto> sortedOptions) {
        OptionGroup optionGroup = optionGroupRepository.findByIdAndMerchantId(optionGroupId, merchantId)
                .orElseThrow(() -> new EntityNotFoundException("OptionGroup não encontrado."));

        List<Option> options = optionGroup.getOptions();

        for (SortRequestDto sortRequest : sortedOptions) {
            options.stream()
                .filter(o -> o.getId().equals(sortRequest.id()))
                .findFirst()
                .ifPresent(o -> o.setIndex(sortRequest.index()));
        }
    
        options.sort(Comparator.comparingInt(Option::getIndex));

        return optionGroupRepository.save(optionGroup);
    }


    
}
