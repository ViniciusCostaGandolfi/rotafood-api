package br.com.rotafood.api.modules.catalog.application.controller.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import br.com.rotafood.api.modules.catalog.application.dto.FullItemDto;
import br.com.rotafood.api.modules.catalog.application.service.CatalogCacheService;
import br.com.rotafood.api.modules.catalog.application.service.CategoryService;
import br.com.rotafood.api.modules.catalog.application.service.ItemService;
import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping(ApiVersion.VERSION + "/merchants/{merchantId}/items")
public class ItemController {

    @Autowired
    private ItemService itemService;

    @Autowired 
    private CatalogCacheService catalogCacheService;

    @Autowired
    public CategoryService categoryService;

    @GetMapping
    public ResponseEntity<List<FullItemDto>> getAllItems(@PathVariable UUID merchantId) {

        var items = categoryService
            .getAllByMerchantIdFromBucket(merchantId)
            .stream()
            .flatMap(cat -> cat.items().stream())      
            .toList();

        return ResponseEntity.ok(items);
    }


    @GetMapping("/{itemId}")
    public ResponseEntity<FullItemDto> getItemById(@PathVariable UUID merchantId, @PathVariable UUID itemId) {
        FullItemDto item = new FullItemDto(itemService.getByIdAndMerchantId(itemId, merchantId));
        return ResponseEntity.ok(item);
    }

    @PutMapping
    public ResponseEntity<FullItemDto> updateOrCreateItem(
            @PathVariable UUID merchantId,
            @RequestBody @Valid FullItemDto FullItemDto) {
        
        FullItemDto updatedItem = new FullItemDto(itemService.updateOrCreate(FullItemDto, merchantId));
        catalogCacheService.updateCatalogCache(merchantId);

        return ResponseEntity.ok(updatedItem);
    }

    @DeleteMapping("/{itemId}")
    public ResponseEntity<Void> deleteItem(@PathVariable UUID merchantId, @PathVariable UUID itemId) {
        itemService.deleteByIdAndMerchantId(itemId, merchantId);
        catalogCacheService.updateCatalogCache(merchantId);

        return ResponseEntity.noContent().build();
    }
}
