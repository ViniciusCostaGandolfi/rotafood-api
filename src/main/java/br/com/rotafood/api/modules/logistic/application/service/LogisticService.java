package br.com.rotafood.api.modules.logistic.application.service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import br.com.rotafood.api.infra.config.redis.RouteCacheService;
import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.logistic.application.dto.CoordinateDto;
import br.com.rotafood.api.modules.logistic.application.dto.DistanceInDto;
import br.com.rotafood.api.modules.logistic.application.dto.DistanceOutDto;
import br.com.rotafood.api.modules.logistic.application.dto.RouteDto;
import br.com.rotafood.api.modules.logistic.application.dto.VrpInDto;
import br.com.rotafood.api.modules.logistic.application.dto.VrpOrderDto;
import br.com.rotafood.api.modules.logistic.application.dto.VrpOriginDto;
import br.com.rotafood.api.modules.logistic.application.dto.VrpOutDto;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantLogisticSetting;


@Service
public class LogisticService {

    @Value("${ROTAFOOD_MS_LOGISTIC_URL}")
    private String logisticServiceUrl;

    @Autowired
    private RestTemplate restTemplate;


    @Autowired
    private RouteCacheService routeCacheService;

    public VrpOutDto logisticRoutesTest(VrpOriginDto origin, Long pointsQuantity) {
        VrpInDto vrpData = generateDataForTest(origin, pointsQuantity, 0.010f);
        String url = this.logisticServiceUrl + "/logistic/vrp";
        ResponseEntity<VrpOutDto> response = restTemplate.postForEntity(url, vrpData, VrpOutDto.class);
        if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
            return response.getBody();
        }

        throw new RuntimeException("Erro ao buscar distância do serviço logístico");
    }

    public VrpInDto generateDataForTest(VrpOriginDto origin, Long pointsQuantity, float std) {
        List<VrpOrderDto> orders = new ArrayList<>();

        for (int i = 0; i < pointsQuantity; i++) {
            var coord = generateRandomCoordinates(origin.address().latitude(), origin.address().longitude(), std);
            AddressDto randomAddress = new AddressDto(
                UUID.randomUUID(),
                origin.address().country(),
                origin.address().state(),
                origin.address().city(),
                origin.address().neighborhood(),
                origin.address().postalCode(),
                origin.address().streetName(),
                origin.address().streetNumber(),
                origin.address().formattedAddress(),
                origin.address().complement(),
                coord.lat(),
                coord.lng()
            );

            var order = new VrpOrderDto(
                UUID.randomUUID(), 
                new BigDecimal(this.generateRandomVolume(5.0, 20.0)),
                new java.util.Date(),
                randomAddress
            );

            orders.add(order);
        }

        return new VrpInDto(UUID.randomUUID(), origin, orders, new BigDecimal(45.0), new Date(System.currentTimeMillis()));
    }

    private CoordinateDto generateRandomCoordinates(BigDecimal lat, BigDecimal lng, float std) {
        double randomLat = lat.doubleValue() + (ThreadLocalRandom.current().nextGaussian() * std);
        double randomLng = lng.doubleValue() + (ThreadLocalRandom.current().nextGaussian() * std);

        return new CoordinateDto(
            BigDecimal.valueOf(randomLat).setScale(6, RoundingMode.HALF_UP),
            BigDecimal.valueOf(randomLng).setScale(6, RoundingMode.HALF_UP)
        );
    }

    private double generateRandomVolume(double min, double max) {
        return ThreadLocalRandom.current().nextDouble(min, max);
    }

    public VrpOutDto logisticRoutesForOrders(VrpInDto vrpInDto) {
        String url = this.logisticServiceUrl + "/logistic/vrp";
        ResponseEntity<VrpOutDto> response = restTemplate.postForEntity(url, vrpInDto, VrpOutDto.class);
        if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
            return response.getBody();
        }

        throw new RuntimeException("Erro ao buscar distância do serviço logístico");
    }



    public RouteDto calculateDistance(AddressDto origin, AddressDto destiny, MerchantLogisticSetting logisticSetting) {
        RouteDto cachedRoute = routeCacheService.getRouteFromCache(origin, destiny);

        if (cachedRoute != null) {
            return cachedRoute;
        }

        DistanceInDto distanceIn = new DistanceInDto(UUID.randomUUID(), origin, destiny);
        String url = this.logisticServiceUrl + "/logistic/distances";

        ResponseEntity<DistanceOutDto> response = restTemplate.postForEntity(url, distanceIn, DistanceOutDto.class);

        if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
            DistanceOutDto distanceDto = response.getBody();

            RouteDto route = new RouteDto(
                distanceDto.id(),
                distanceDto.origin(),
                distanceDto.destiny(),
                distanceDto.distanceMeters(),
                this.calculateDeliveryFee(distanceDto.distanceMeters(), logisticSetting),
                distanceDto.routeLine()
            );

            routeCacheService.saveRouteToCache(origin, destiny, route);

            return route;
        }

        throw new RuntimeException("Erro ao buscar distância do serviço logístico");
    }


    
    public BigDecimal calculateDeliveryFee(BigDecimal distanceMeters, MerchantLogisticSetting logisticSetting) {
        if (distanceMeters == null || logisticSetting == null) {
            return BigDecimal.ZERO;
        }
    
        BigDecimal distanceKm = distanceMeters
                .divide(BigDecimal.valueOf(1000), 2, RoundingMode.UP);
    
        BigDecimal fee = logisticSetting.getDeliveryFeePerKm().multiply(distanceKm);
    
        BigDecimal roundingFactor = new BigDecimal("0.50");
        BigDecimal remainder = fee.remainder(roundingFactor);
    
        if (remainder.compareTo(BigDecimal.ZERO) > 0) {
            fee = fee.add(roundingFactor.subtract(remainder));
        }
    
        if (fee.compareTo(logisticSetting.getMinDeliveryFee()) < 0) {
            fee = logisticSetting.getMinDeliveryFee();
        }
    
        return fee.setScale(2, RoundingMode.UP);
    }
    
    
    

}
