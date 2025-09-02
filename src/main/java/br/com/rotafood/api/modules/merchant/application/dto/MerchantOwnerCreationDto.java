package br.com.rotafood.api.modules.merchant.application.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;

public record MerchantOwnerCreationDto (
    @NotNull() @Valid
    MerchantCreateDto merchant,
    
    @NotNull() @Valid
    OwnerCreateDto owner
) {}
