package br.com.rotafood.api.modules.merchant.application.dto;

import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record MerchantUserCreateDto(
    @NotBlank
    String name,
    @NotBlank
    String email,
    @NotBlank
    String phone,
    @NotBlank
    String password,
    @NotNull
    MerchantUserRole role
) {}
