package br.com.rotafood.api.infra.security;


import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;

import br.com.rotafood.api.modules.merchant.application.dto.MerchantUserDto;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;

import java.util.Arrays;

@Aspect
@Component
public class MerchantRoleAllowedAspect {

    @Around("@annotation(merchantRoleAllowed)")
    public Object checkRole(ProceedingJoinPoint pjp, MerchantRoleAllowed merchantRoleAllowed) throws Throwable {
        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();

        if (principal instanceof MerchantUserDto userDto) {
            MerchantUserRole userRole = userDto.role();
            MerchantUserRole[] allowedRoles = merchantRoleAllowed.value();

            boolean isAllowed = Arrays.asList(allowedRoles).contains(userRole);
            if (!isAllowed) {
                throw new ResponseStatusException(HttpStatus.FORBIDDEN,
                    "Acesso negado: é necessário ter uma das roles " + Arrays.toString(allowedRoles));
            }
        } else {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Usuário não autenticado");
        }

        return pjp.proceed();
    }
}