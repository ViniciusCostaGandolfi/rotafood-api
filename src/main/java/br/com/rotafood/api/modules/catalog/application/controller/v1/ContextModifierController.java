package br.com.rotafood.api.modules.catalog.application.controller.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import br.com.rotafood.api.modules.catalog.application.dto.ContextModifierDto;
import br.com.rotafood.api.modules.catalog.application.service.CatalogCacheService;
import br.com.rotafood.api.modules.catalog.application.service.ContextModifierService;
import jakarta.validation.Valid;
import java.util.UUID;

@RestController
@RequestMapping( ApiVersion.VERSION + "/merchants/{merchantId}/contextModifiers")
public class ContextModifierController {

    @Autowired
    private ContextModifierService contextModifierService;

    @Autowired 
    private CatalogCacheService catalogCacheService;

    @PutMapping
    public ContextModifierDto updateOrCreate(
            @PathVariable UUID merchantId,
            @RequestBody @Valid ContextModifierDto contextModifierDto) {
        var cm = new ContextModifierDto(contextModifierService.updateOrCreate(contextModifierDto, null, null, null));
        catalogCacheService.updateOrCreateContextModifier(merchantId, cm);
        return cm;
    }

}
