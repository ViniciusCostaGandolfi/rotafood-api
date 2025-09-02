package br.com.rotafood.api.modules.order.application.validator;

import java.util.List;

import org.springframework.stereotype.Component;

import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.order.application.dto.FullOrderDto;
import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class OrderValidationEngine {

    private final List<OrderValidator> validators;

    public void validate(FullOrderDto dto, Merchant merchant) {
        validators.stream()
                    .filter(v  -> v.supports(dto))
                    .forEach(v -> v.validate(dto, merchant));
    }
}

