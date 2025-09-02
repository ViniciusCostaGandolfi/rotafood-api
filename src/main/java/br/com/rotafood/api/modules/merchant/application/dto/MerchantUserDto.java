package br.com.rotafood.api.modules.merchant.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUser;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;

public record MerchantUserDto(
    UUID id,
    String name,
    String email,
    String phone,
    MerchantUserRole role,
    UUID merchantId
) {
    public MerchantUserDto(MerchantUser merchantUser) {
        this(
            merchantUser.getId(),
            merchantUser.getName(),
            merchantUser.getEmail(),
            merchantUser.getPhone(),
            merchantUser.getRole(),
            merchantUser.getMerchant().getId()
        );
    }
}
