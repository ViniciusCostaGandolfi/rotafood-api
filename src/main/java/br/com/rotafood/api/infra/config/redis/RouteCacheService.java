
package br.com.rotafood.api.infra.config.redis;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.logistic.application.dto.RouteDto;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;

@Service
public class RouteCacheService {

    private static final String PREFIX = "route:";
    private static final long TTL_MINUTES = 5;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;


    public RouteDto getRouteFromCache(AddressDto origin, AddressDto destination) {
        String key = generateKey(origin, destination);
        return (RouteDto) redisTemplate.opsForValue().get(key);
    }

    public void saveRouteToCache(AddressDto origin, AddressDto destination, RouteDto route) {
        String key = generateKey(origin, destination);
        redisTemplate.opsForValue().set(key, route, Duration.ofMinutes(TTL_MINUTES));
    }

    private String generateKey(AddressDto origin, AddressDto destination) {
        return PREFIX + hash(origin) + ":" + hash(destination);
    }

    private String hash(AddressDto address) {
        return String.valueOf((address.formattedAddress() + address.latitude() + address.longitude()).hashCode());
    }
}

