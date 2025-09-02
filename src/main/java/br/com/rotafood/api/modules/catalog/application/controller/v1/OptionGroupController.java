package br.com.rotafood.api.modules.catalog.application.controller.v1;

import br.com.rotafood.api.modules.catalog.application.dto.OptionGroupDto;
import br.com.rotafood.api.modules.catalog.application.dto.SortRequestDto;
import br.com.rotafood.api.modules.catalog.application.service.CatalogCacheService;
import br.com.rotafood.api.modules.catalog.application.service.OptionGroupService;
import br.com.rotafood.api.modules.catalog.application.service.OptionService;
import br.com.rotafood.api.modules.catalog.domain.entity.OptionGroupType;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping( ApiVersion.VERSION + "/merchants/{merchantId}/optionGroups")
public class OptionGroupController {

    @Autowired
    private OptionGroupService optionGroupService;

    @Autowired
    private OptionService optionService;

    @Autowired 
    private CatalogCacheService catalogCacheService;

    @GetMapping
    public List<OptionGroupDto> getAll(
            @PathVariable UUID merchantId,
            @RequestParam(required = false) OptionGroupType optionGroupType) {
        
        if (optionGroupType != null) {
            return optionGroupService.getAllByMerchantIdAndOptionGroupType(merchantId, optionGroupType)
                    .stream()
                    .map(OptionGroupDto::new)
                    .toList();
        }

        
        return optionGroupService.getAllByMerchantId(merchantId)
                .stream()
                .map(OptionGroupDto::new)
                .toList();
    }

    @GetMapping("/{optionGroupId}")
    public OptionGroupDto getById(@PathVariable UUID merchantId, @PathVariable UUID optionGroupId) {
        return new OptionGroupDto(optionGroupService.getByIdAndMerchantId(optionGroupId, merchantId));
    }

    @PutMapping
    public OptionGroupDto updateOrCreate(
            @PathVariable UUID merchantId,
            @RequestBody @Valid OptionGroupDto optionGroupDto) {
        
                catalogCacheService.updateCatalogCache(merchantId);
        return new OptionGroupDto(optionGroupService.updateOrCreate(optionGroupDto, merchantId));
    }

    @DeleteMapping("/{optionGroupId}")
    public void delete(@PathVariable UUID merchantId, @PathVariable UUID optionGroupId) {
        optionGroupService.deleteByIdAndMerchantId(optionGroupId, merchantId);
    }

    @PutMapping("/{optionGroupId}/options/sort")
    public ResponseEntity<Void> updateOrCreateOption(
            @PathVariable UUID merchantId,
            @PathVariable UUID optionGroupId,
            @RequestBody List<SortRequestDto> sortedOptions
            ) {
        
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{optionGroupId}/options/{optionId}")
    public void deleteOption(@PathVariable UUID merchantId, @PathVariable UUID optionId) {
        optionService.deleteByIdAndMerchantId(optionId, merchantId);
    }
}
