package br.com.rotafood.api.modules.order.application.controller.v1;

import br.com.rotafood.api.infra.security.MerchantRoleAllowed;
import br.com.rotafood.api.infra.utils.PaginationDto;
import br.com.rotafood.api.modules.merchant.application.service.MerchantService;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;
import br.com.rotafood.api.modules.order.application.dto.FullOrderDto;
import br.com.rotafood.api.modules.order.application.dto.OrderDto;
import br.com.rotafood.api.modules.order.application.service.OrderService;
import br.com.rotafood.api.modules.order.domain.entity.OrderSalesChannel;
import br.com.rotafood.api.modules.order.domain.entity.OrderStatus;
import br.com.rotafood.api.modules.order.domain.entity.OrderType;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping(ApiVersion.VERSION + "/merchants/{merchantId}/orders")
public class OrderController {

    @Autowired
    private OrderService orderService;

    @Autowired
    private MerchantService merchantService;

    @MerchantRoleAllowed({MerchantUserRole.OWNER, MerchantUserRole.ADMIN})
    @GetMapping
    public ResponseEntity<PaginationDto<OrderDto>> getAllOrders(
        @PathVariable UUID merchantId,
        @RequestParam(required = false) List<OrderType> orderTypes,
        @RequestParam(required = false) List<OrderStatus> orderStatuses,
        @RequestParam(required = false) String startDate,
        @RequestParam(required = false) String endDate,
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "100") int size,
        @RequestParam(defaultValue = "createdAt") String sortBy,
        @RequestParam(defaultValue = "desc") String sortDirection) {
        

        Pageable pageable = PageRequest.of(page, size, Sort.by(
            sortDirection.equalsIgnoreCase("desc") ? Sort.Direction.DESC : Sort.Direction.ASC, sortBy));

        Page<OrderDto> orders = orderService.getAllByFilters(
            merchantId, orderTypes, orderStatuses, startDate, endDate, pageable
        ).map(OrderDto::new);

        return ResponseEntity.ok(PaginationDto.fromPage(orders, "/orders"));
    }

    @GetMapping("/polling")
    public ResponseEntity<List<FullOrderDto>> polling(
        @PathVariable UUID merchantId,
        @RequestParam(defaultValue = "ROTAFOOD") List<OrderSalesChannel> sources) {

        merchantService.updateMerchantOpened(merchantId, sources, true);

        List<FullOrderDto> orders = orderService.polling(
            merchantId
        );

        return ResponseEntity.ok(orders);
    }

    @GetMapping("/polling/stop")
    public ResponseEntity<Void> stopPolling(
        @PathVariable UUID merchantId,
        @RequestParam(defaultValue = "ROTAFOOD") List<OrderSalesChannel> sources) {

        merchantService.updateMerchantOpened(merchantId, sources, false);


        return ResponseEntity.noContent().build();
    }

    @PutMapping("/{orderId}/status/{status}")
    public ResponseEntity<Void> updateOrderStatus(
            @PathVariable UUID merchantId,
            @PathVariable UUID orderId,
            @PathVariable OrderStatus status) {
        orderService.updateOrderStatus(merchantId, orderId, status);
        return ResponseEntity.ok().build();
    }


    @PutMapping("/{orderId}/printed/{printed}")
    public ResponseEntity<Void> updateOrderPrinted(
            @PathVariable UUID merchantId,
            @PathVariable UUID orderId,
            @PathVariable boolean printed) {
        orderService.updateOrderPrinted(merchantId, orderId, printed);
        return ResponseEntity.ok().build();
    }


    @GetMapping("/{orderId}")
    public FullOrderDto getOrderById(@PathVariable UUID merchantId, @PathVariable UUID orderId) {
        return new FullOrderDto(orderService.getByIdAndMerchantId(orderId, merchantId));
    }

    @PutMapping
    public FullOrderDto createOrUpdateOrder(
            @PathVariable UUID merchantId,
            @RequestBody @Valid FullOrderDto fullOrderDto) {
        return new FullOrderDto(orderService.createOrUpdate(fullOrderDto, merchantId));
    }


    @DeleteMapping("/{orderId}")
    public void deleteOrder(@PathVariable UUID merchantId, @PathVariable UUID orderId) {
        orderService.deleteByIdAndMerchantId(orderId, merchantId);
    }
}
