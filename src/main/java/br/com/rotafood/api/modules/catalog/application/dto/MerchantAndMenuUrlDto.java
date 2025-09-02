package br.com.rotafood.api.modules.catalog.application.dto;

import br.com.rotafood.api.modules.merchant.application.dto.FullMerchantDto;

public record MerchantAndMenuUrlDto(
    FullMerchantDto merchant,
    String menuUrl
) {
    
}
