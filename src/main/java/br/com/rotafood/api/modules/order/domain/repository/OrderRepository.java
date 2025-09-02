package br.com.rotafood.api.modules.order.domain.repository;

import jakarta.transaction.Transactional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderStatus;
import br.com.rotafood.api.modules.order.domain.entity.OrderTiming;
import br.com.rotafood.api.modules.order.domain.entity.OrderType;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface OrderRepository extends JpaRepository<Order, UUID> {
    
    List<Order> findAllByMerchantId(UUID merchantId);

    Optional<Order> findByIdAndMerchantId(UUID id, UUID merchantId);

    @Query("SELECT o FROM Order o " +
        "WHERE o.merchant.id = :merchantId " +
        "AND (:orderTypes IS NULL OR o.type IN :orderTypes) " +
        "AND (:orderStatuses IS NULL OR o.status IN :orderStatuses) " +
        "AND (COALESCE(:startDate, NULL) IS NULL OR o.createdAt >= :startDate) " +
        "AND (COALESCE(:endDate, NULL) IS NULL OR o.createdAt <= :endDate)")
    Page<Order> findAllByFilters(
        @Param("merchantId") UUID merchantId,
        @Param("orderTypes") List<OrderType> orderTypes,
        @Param("orderStatuses") List<OrderStatus> orderStatuses,  
        @Param("startDate") Instant startDate,
        @Param("endDate") Instant endDate,
        Pageable pageable);

    @Modifying
    @Transactional
    @Query("UPDATE Order o SET o.status = :status WHERE o.id = :orderId AND o.merchant.id = :merchantId")
    int updateOrderStatus(@Param("merchantId") UUID merchantId, 
                          @Param("orderId") UUID orderId, 
                          @Param("status") OrderStatus status);


    @Modifying
    @Transactional
    @Query("UPDATE Order o SET o.printed = :printed WHERE o.id = :orderId AND o.merchant.id = :merchantId")
    int updateOrderPrinted(@Param("merchantId") UUID merchantId, 
                          @Param("orderId") UUID orderId, 
                          @Param("printed") boolean printed);


    List<Order> findByPreparationStartDateTimeBeforeAndStatusNotAndTiming(
            Instant cutoffTime, 
            OrderStatus status, 
            OrderTiming timing);

    @Query("""
        SELECT MAX(o.merchantSequence) 
          FROM Order o 
         WHERE o.merchant.id = :merchantId
    """)
    Long findMaxMerchantSequenceByMerchantId(UUID merchantId);



    @Query("""
        SELECT o FROM Order o
        WHERE o.merchant.id = :merchantId
        AND o.status IN :statuses
        AND o.createdAt >= :start
    """)
    List<Order> findRecentOrdersByStatus(
        @Param("merchantId") UUID merchantId,
        @Param("statuses") List<OrderStatus> statuses,
        @Param("start") Instant start
    );




}
