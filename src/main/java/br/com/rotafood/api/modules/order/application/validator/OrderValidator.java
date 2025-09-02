package br.com.rotafood.api.modules.order.application.validator;

import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.order.application.dto.FullOrderDto;

public interface OrderValidator {

    void validate(FullOrderDto dto, Merchant merchant);

    boolean supports(FullOrderDto dto);
}