package br.com.rotafood.api.modules.order.application.validator;

import org.springframework.stereotype.Component;

import br.com.rotafood.api.infra.utils.DistanceUtils;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.order.application.dto.FullOrderDto;
import br.com.rotafood.api.modules.order.domain.entity.OrderType;
import jakarta.validation.ValidationException;
import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class DeliveryRadiusValidator implements OrderValidator {


    @Override
    public boolean supports(FullOrderDto dto) {
        return dto.type() == OrderType.DELIVERY
            && dto.delivery() != null
            && dto.delivery().address() != null;
    }

    @Override
    public void validate(FullOrderDto dto, Merchant merchant) {

        var ls = merchant.getLogisticSetting();
        if (ls == null || ls.getMaxDeliveryRadiusKm() == null) return;

        double maxKm = ls.getMaxDeliveryRadiusKm().doubleValue();

        double originLat = ls.getLatitude() != null
                ? ls.getLatitude().doubleValue()
                : merchant.getAddress().getLatitude().doubleValue();
        double originLon = ls.getLongitude() != null
                ? ls.getLongitude().doubleValue()
                : merchant.getAddress().getLongitude().doubleValue();

        var dest = dto.delivery().address();
        double dKm = DistanceUtils.haversineKm(
                originLat, originLon,
                dest.latitude().doubleValue(), dest.longitude().doubleValue());

        if (dKm > maxKm) {
            throw new ValidationException(
                String.format("Endereço fora da área de entrega (%.2f km > %.2f km)",
                                dKm, maxKm));
        }
    }
}

