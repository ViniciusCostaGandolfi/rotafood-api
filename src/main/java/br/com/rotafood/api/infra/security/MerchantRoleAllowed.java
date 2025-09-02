package br.com.rotafood.api.infra.security;


import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;



@Target({ElementType.METHOD, ElementType.TYPE}) 
@Retention(RetentionPolicy.RUNTIME)
public @interface MerchantRoleAllowed {
    MerchantUserRole[] value();
}