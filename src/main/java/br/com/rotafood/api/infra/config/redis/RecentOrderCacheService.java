package br.com.rotafood.api.infra.config.redis;

import java.time.Duration;
import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;

import br.com.rotafood.api.modules.order.application.dto.FullOrderDto;

@Service
public class RecentOrderCacheService {

    private static final Duration TTL = Duration.ofHours(2);

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @Autowired
    private ObjectMapper objectMapper;

    private String getKey(UUID merchantId) {
        return "order:polling:merchant:" + merchantId;
    }

    public void addOrUpdateRecentOrder(UUID merchantId, FullOrderDto orderDto) {
        List<FullOrderDto> current = getCachedRecentOrders(merchantId);

        if (current != null) {
            current.removeIf(o -> o.id().equals(orderDto.id()));
        } else {
            current = new java.util.ArrayList<>();
        }

        current.add(0, orderDto);
        cacheRecentOrders(merchantId, current);
    }

    public List<FullOrderDto> getCachedRecentOrders(UUID merchantId) {
        String json = redisTemplate.opsForValue().get(getKey(merchantId));
        if (json == null) return List.of();

        try {
            JavaType type = objectMapper.getTypeFactory().constructCollectionType(List.class, FullOrderDto.class);
            return objectMapper.readValue(json, type);
        } catch (Exception e) {
            return List.of();
        }
    }

    public Long getNextMerchantSequenceFromCache(UUID merchantId) {
        List<FullOrderDto> orders = getCachedRecentOrders(merchantId);
        if (orders == null || orders.isEmpty()) return null;

        return orders.stream()
                .map(FullOrderDto::merchantSequence)
                .filter(seq -> seq != null)
                .max(Long::compareTo)
                .orElse(0L) + 1;
    }

    public void cacheRecentOrders(UUID merchantId, List<FullOrderDto> orders) {
        try {
            String json = objectMapper.writeValueAsString(orders);
            redisTemplate.opsForValue().set(getKey(merchantId), json, TTL);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Erro ao serializar lista de orders para Redis", e);
        }
    }

    public void clearRecentOrders(UUID merchantId) {
        redisTemplate.delete(getKey(merchantId));
    }
}
