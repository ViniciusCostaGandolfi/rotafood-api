package br.com.rotafood.api.modules.merchant.application.controller.v1;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.rotafood.api.infra.security.MerchantRoleAllowed;
import br.com.rotafood.api.modules.merchant.application.dto.MerchantUserCreateDto;
import br.com.rotafood.api.modules.merchant.application.dto.MerchantUserDto;
import br.com.rotafood.api.modules.merchant.application.dto.MerchantUserUpdateDto;
import br.com.rotafood.api.modules.merchant.application.service.MerchantUserService;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;
import jakarta.validation.Valid;

@MerchantRoleAllowed({MerchantUserRole.OWNER, MerchantUserRole.ADMIN})
@RestController
@RequestMapping(ApiVersion.VERSION + "/merchants/{merchantId}/users")
public class MerchantUserController {

    @Autowired
    private MerchantUserService merchantUserService;

    @GetMapping
    public List<MerchantUserDto> list(@PathVariable UUID merchantId) {
        return merchantUserService.getUsersByMerchantId(merchantId).stream()
            .filter(user -> user.getRole() != MerchantUserRole.OWNER)
            .map(MerchantUserDto::new)
            .toList();
    }
    


    @PostMapping
    public MerchantUserDto create(
        @PathVariable UUID merchantId,
        @Valid @RequestBody MerchantUserCreateDto dto
    ) {
        return new MerchantUserDto(merchantUserService.createMerchantUser(merchantId, dto));
    }

    @PutMapping("/{merchantUserId}")
    public MerchantUserDto update(
        @PathVariable UUID merchantId,
        @PathVariable UUID merchantUserId,
        @Valid @RequestBody MerchantUserUpdateDto dto
    ) {
        return new MerchantUserDto(merchantUserService.updateMerchantUser(merchantId, merchantUserId, dto));
    }

    @DeleteMapping("/{merchantUserId}")
    public MerchantUserDto delete(
        @PathVariable UUID merchantId,
        @PathVariable UUID merchantUserId
    ) {
        return new MerchantUserDto(merchantUserService.deleteMerchantUser(merchantId, merchantUserId));
    }
}
