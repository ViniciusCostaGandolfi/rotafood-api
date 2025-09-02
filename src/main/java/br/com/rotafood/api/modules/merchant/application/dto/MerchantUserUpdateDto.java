package br.com.rotafood.api.modules.merchant.application.dto;

import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public record MerchantUserUpdateDto(
    
    @NotBlank(message = "Nome é obrigatório")
    String name,

    @NotBlank(message = "Email é obrigatório")
    @Email(message = "Email inválido")
    String email,

    @NotBlank(message = "Telefone é obrigatório")
    @Pattern(regexp = "\\d{10,15}", message = "Telefone deve conter entre 10 e 15 dígitos")
    String phone,

    @NotNull
    MerchantUserRole role
) {}
