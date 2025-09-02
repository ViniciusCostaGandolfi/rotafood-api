package br.com.rotafood.api.modules.catalog.application.controller.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.rotafood.api.modules.catalog.application.service.CatalogCacheService;
import br.com.rotafood.api.modules.catalog.application.service.OptionService;

import java.util.UUID;

@RestController
@RequestMapping(ApiVersion.VERSION + "/merchants/{merchantId}/options")
public class OptionController {

    @Autowired
    private OptionService optionService;

    @Autowired 
    private CatalogCacheService catalogCacheService;

    @DeleteMapping("/{optionId}")
    public void deleteOption(@PathVariable UUID merchantId, @PathVariable UUID optionId) {

        catalogCacheService.updateCatalogCache(merchantId);
        optionService.deleteByIdAndMerchantId(optionId, merchantId);
    }
}
