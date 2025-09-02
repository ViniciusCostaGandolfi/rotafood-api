package br.com.rotafood.api.modules.order.application.validator;

import br.com.rotafood.api.modules.catalog.domain.entity.ContextModifier;
import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.logistic.application.dto.RouteDto;
import br.com.rotafood.api.modules.logistic.application.service.LogisticService;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.ContextModifierRepository;
import br.com.rotafood.api.modules.order.application.dto.FullOrderDto;
import br.com.rotafood.api.modules.order.application.dto.OrderItemDto;
import br.com.rotafood.api.modules.order.application.dto.OrderItemOptionDto;
import jakarta.validation.ValidationException;
import lombok.RequiredArgsConstructor;

import java.math.BigDecimal;

import org.springframework.stereotype.Component;


@Component
@RequiredArgsConstructor
public class OrderTotalValidator implements OrderValidator {

    private final ContextModifierRepository contextModifierRepository;
    private final LogisticService          logisticService;

    @Override
    public boolean supports(FullOrderDto dto) {
        return dto.items() != null && !dto.items().isEmpty();
    }

    @Override
    public void validate(FullOrderDto dto, Merchant merchant) {
        BigDecimal subtotal        = BigDecimal.ZERO;
        BigDecimal additionalFees  = BigDecimal.ZERO;
        BigDecimal benefits        = BigDecimal.ZERO;
        BigDecimal deliveryFee     = BigDecimal.ZERO;

        for (OrderItemDto item : dto.items()) {

            ContextModifier cmItem = contextModifierRepository
                    .findById(item.contextModifierId())
                    .orElseThrow(() -> new ValidationException(
                            "ContextModifier não encontrado: " + item.contextModifierId()));

            BigDecimal base = cmItem.getPrice().getValue();
            BigDecimal opts = BigDecimal.ZERO;

            if (item.options() != null) {
                for (OrderItemOptionDto op : item.options()) {
                    ContextModifier cmOp = contextModifierRepository
                            .findById(op.contextModifierId())
                            .orElseThrow(() -> new ValidationException(
                                    "ContextModifier não encontrado: " + op.contextModifierId()));

                    opts = opts.add(cmOp.getPrice()
                                        .getValue()
                                        .multiply(BigDecimal.valueOf(op.quantity())));
                }
            }

            subtotal = subtotal.add(base.add(opts)
                                        .multiply(BigDecimal.valueOf(item.quantity())));
                                        
        }

        if (dto.additionalFees() != null) {
            additionalFees = dto.additionalFees().stream()
                                        .map(f -> f.value())
                                        .reduce(BigDecimal.ZERO, BigDecimal::add);
        }

        if (dto.benefits() != null) {
            benefits = dto.benefits().stream()
                                .map(b -> b.value())
                                .reduce(BigDecimal.ZERO, BigDecimal::add);
        }

        if (dto.delivery() != null) {
            AddressDto origin      = new AddressDto(merchant.getAddress());
            AddressDto destination = dto.delivery().address();

            RouteDto route = logisticService
                    .calculateDistance(origin, destination, merchant.getLogisticSetting());

            deliveryFee = route.deliveryFee();
        }

        BigDecimal orderAmount = subtotal
                .add(additionalFees)
                .add(deliveryFee)
                .subtract(benefits);

        boolean mismatch =
                dto.total().subTotal().compareTo(subtotal)            != 0 ||
                dto.total().deliveryFee().compareTo(deliveryFee)      != 0 ||
                dto.total().additionalFees().compareTo(additionalFees)    != 0 ||
                dto.total().benefits().compareTo(benefits)            != 0 ||
                dto.total().orderAmount().compareTo(orderAmount)      != 0;

        if (mismatch)
            throw new ValidationException("Totais enviados não conferem com os valores calculados.");
    }

}
