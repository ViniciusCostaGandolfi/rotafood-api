package br.com.rotafood.api.modules.catalog.application.controller.v1;


import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.rotafood.api.modules.catalog.application.dto.CategoryDto;
import br.com.rotafood.api.modules.catalog.application.dto.FullCategoryDto;
import br.com.rotafood.api.modules.catalog.application.dto.SortRequestDto;
import br.com.rotafood.api.modules.catalog.application.service.CatalogCacheService;
import br.com.rotafood.api.modules.catalog.application.service.CategoryService;
import jakarta.validation.Valid;

@RestController
@RequestMapping( ApiVersion.VERSION + "/merchants/{merchantId}/categories")
public class CategoryController {

    @Autowired
    private CategoryService categoryService;

    @Autowired 
    private CatalogCacheService catalogCacheService;
  
    @GetMapping
    public List<FullCategoryDto> getAll(
        @PathVariable UUID merchantId
    ) {
        return categoryService.getAllByMerchantIdFromBucket(merchantId);
    }

  
    @GetMapping("simplified")
    public List<CategoryDto> getAllSimplied(
        @PathVariable UUID merchantId
    ) {
        return categoryService.getAllByMerchantId(merchantId).stream()
            .map(CategoryDto::new)
            .toList();
    }

  
    @GetMapping("/{categoryId}")
    public FullCategoryDto getById(
        @PathVariable UUID merchantId,
        @PathVariable UUID categoryId
    ) {
        return new FullCategoryDto(
            categoryService.getByIdAndMerchantId(categoryId, merchantId)
            );
    }

  
    @DeleteMapping("/{categoryId}")
    public void deleteById(
        @PathVariable UUID merchantId,
        @PathVariable UUID categoryId
    ) {
        categoryService.deleteByIdAndMerchantId(categoryId, merchantId);

        catalogCacheService.updateCatalogCache(merchantId);

    }

  
    @PutMapping
    public FullCategoryDto updateOrCreate(
        @PathVariable UUID merchantId,
        @RequestBody @Valid CategoryDto categoryDto
    ) {
        var category = categoryService.updateOrCreate(categoryDto, merchantId);

        catalogCacheService.updateCatalogCache(merchantId);

        return new FullCategoryDto(category);
    }


   
    @PutMapping("/{categoryId}/items/sort")
    public ResponseEntity<Void> sortItemsInCategory(
        @PathVariable UUID merchantId,
        @PathVariable UUID categoryId,
        @RequestBody List<SortRequestDto> sortedItems
    ) {
        categoryService.sortItemsInCategory(merchantId, categoryId, sortedItems);

        catalogCacheService.updateCatalogCache(merchantId);


        return ResponseEntity.ok().build();
    }

  
    @PutMapping("/sort")
    public ResponseEntity<Void> sortCategories(
        @PathVariable UUID merchantId,
        @RequestBody List<SortRequestDto> sortedCategories
    ) {
        categoryService.sortCategories(merchantId, sortedCategories);

        catalogCacheService.updateCatalogCache(merchantId);

        return ResponseEntity.ok().build();
    }

}
