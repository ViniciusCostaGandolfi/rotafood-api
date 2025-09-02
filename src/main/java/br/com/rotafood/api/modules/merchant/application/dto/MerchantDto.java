package br.com.rotafood.api.modules.merchant.application.dto;

import java.time.Instant;
import java.util.UUID;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.merchant.domain.entity.DocumentType;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantType;

public record MerchantDto (
    UUID id,
    String name,
    String onlineName,
    String imagePath,
    String description,
    DocumentType documentType,
    String document,
    String phone,
    MerchantType merchantType,
    Instant createdAt,
    Instant lastOpenedUtc,
    AddressDto address
    ) {

    public MerchantDto(Merchant merchant) {
       this(merchant.getId(), 
       merchant.getName(), 
       merchant.getOnlineName(),
       merchant.getImagePath(),
       merchant.getDescription(), 
       merchant.getDocumentType(), 
       merchant.getDocument(), 
       merchant.getPhone(),
       merchant.getMerchantType(), 
       merchant.getCreatedAt(), 
       merchant.getLastOpenedUtc(),
       new AddressDto(merchant.getAddress()));
    }
}
