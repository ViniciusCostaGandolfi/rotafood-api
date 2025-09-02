package br.com.rotafood.api.modules.catalog.application.service;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.rotafood.api.modules.catalog.application.dto.CategoryDto;
import br.com.rotafood.api.modules.catalog.application.dto.FullItemDto;
import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.Category;
import br.com.rotafood.api.modules.catalog.domain.entity.Item;
import br.com.rotafood.api.modules.catalog.domain.entity.TemplateType;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.ItemRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;

@Service
public class ItemService {

    @Autowired private ProductService productService;
    @Autowired private ItemRepository itemRepository;
    @Autowired private MerchantRepository merchantRepository;
    @Autowired private CategoryService categoryService;
    @Autowired private ShiftService shiftService;
    @Autowired private ContextModifierService contextModifierService;
    @Autowired private ItemOptionGroupService itemOptionGroupService;

    public Item getByIdAndMerchantId(UUID id, UUID merchantId) {
        return itemRepository.findByIdAndMerchantId(id, merchantId)
                .orElseThrow(() -> new EntityNotFoundException("Item não encontrado."));
    }

    @Transactional
    public Item updateOrCreate(FullItemDto itemDto, UUID merchantId) {
        if (itemDto.type() == TemplateType.PIZZA) {
            return updateOrCreatePizza(itemDto, merchantId);
        }
        return updateOrCreateRegular(itemDto, merchantId);
    }

    private Item updateOrCreateRegular(FullItemDto itemDto, UUID merchantId) {
        Item item = itemDto.id() != null
                ? getByIdAndMerchantId(itemDto.id(), merchantId)
                : new Item();

        Merchant merchant = merchantRepository.getReferenceById(merchantId);
        Category category = categoryService.getByIdAndMerchantId(itemDto.categoryId(), merchantId);

        item.setMerchant(merchant);
        item.setCategory(category);
        item.setType(itemDto.type());
        item.setStatus(itemDto.status());
        item.setIndex(itemDto.index());
        item.setProduct(productService.updateOrCreate(itemDto.product(), merchantId));

        itemRepository.save(item);

        itemDto.contextModifiers().forEach(cm -> {
            this.contextModifierService.updateOrCreate(cm, item, null, null);
        });

        if (itemDto.optionGroups() != null) {
            itemOptionGroupService.createOrUpdateAll(itemDto.optionGroups(), item, merchantId, false);
        }

        if (itemDto.shifts() != null) {
            itemDto.shifts().forEach(sh -> {
                this.shiftService.updateOrCreate(sh, item, null);
            });
        }

        return item;
    }

    @Transactional
    public Item updateOrCreatePizza(FullItemDto itemDto, UUID merchantId) {
        Item item = itemDto.id() != null
                ? getByIdAndMerchantId(itemDto.id(), merchantId)
                : new Item();

        Merchant merchant = merchantRepository.getReferenceById(merchantId);

        Category category = itemDto.categoryId() != null ?
                categoryService.getByIdAndMerchantId(itemDto.categoryId(), merchantId) :
                categoryService.updateOrCreate(new CategoryDto(null, 1, itemDto.product().name(), TemplateType.PIZZA, AvailabilityStatus.AVAILIABLE), merchantId);

        item.setMerchant(merchant);
        item.setCategory(category);
        item.setType(TemplateType.PIZZA);
        item.setStatus(itemDto.status());

        item.setIndex(1);

        item.setProduct(productService.updateOrCreate(itemDto.product(), merchantId));
        itemRepository.save(item);

        itemDto.contextModifiers().forEach(cm -> {
            this.contextModifierService.updateOrCreate(cm, item, null, null);
        });

        if (itemDto.shifts() != null) {
            itemDto.shifts().forEach(sh -> {
                this.shiftService.updateOrCreate(sh, item, null);
            });
        }

        if (itemDto.optionGroups() != null) {
            itemOptionGroupService.createOrUpdateAll(itemDto.optionGroups(), item, merchantId, true);
        }

        return item;
    }

    @Transactional
    public void deleteByIdAndMerchantId(UUID itemId, UUID merchantId) {
        Item item = getByIdAndMerchantId(itemId, merchantId);
        itemRepository.delete(item);
    }

    public List<Item> getAllByMerchantId(UUID merchantId) {
        return itemRepository.findAllByMerchantId(merchantId);
    }
}
