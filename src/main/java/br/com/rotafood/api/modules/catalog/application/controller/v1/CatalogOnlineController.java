package br.com.rotafood.api.modules.catalog.application.controller.v1;


import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import br.com.rotafood.api.modules.catalog.application.dto.FullCategoryDto;
import br.com.rotafood.api.modules.catalog.application.service.CategoryService;
import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.logistic.application.dto.RouteDto;
import br.com.rotafood.api.modules.logistic.application.service.LogisticService;
import br.com.rotafood.api.modules.merchant.application.dto.FullMerchantDto;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import br.com.rotafood.api.modules.order.application.dto.FullOrderDto;
import br.com.rotafood.api.modules.order.application.service.OrderService;
import jakarta.validation.Valid;

import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@RequestMapping( ApiVersion.VERSION + "/catalogs/online")
public class CatalogOnlineController {

    @Autowired
    private LogisticService logisticService;

    @Autowired
    private MerchantRepository merchantRepository;

    @Autowired
    private OrderService orderService;

    @Autowired
    private CategoryService categoryService;

    @GetMapping("/{onlineName}")
    public FullMerchantDto getMerchant(
        @PathVariable String onlineName
    ) {
        return new FullMerchantDto(this.merchantRepository.findByOnlineName(onlineName)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Merchant not found")));
    }


    @GetMapping("/{onlineName}/categories")
    public List<FullCategoryDto> getCategories(
        @PathVariable String onlineName
    ) {
        var merchant = merchantRepository
            .findByOnlineName(onlineName)
            .orElseThrow(() -> new ResponseStatusException(
                HttpStatus.NOT_FOUND, "Merchant not found"));

        return categoryService.getAllByMerchantIdFromBucket(merchant.getId());
    }

    @GetMapping("/{onlineName}/orders/{orderId}")
    public FullOrderDto getOrderById(@PathVariable String onlineName, @PathVariable UUID orderId) {
        var merchant = new FullMerchantDto(this.merchantRepository.findByOnlineName(onlineName)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Merchant not found")));

        return new FullOrderDto(orderService.getByIdAndMerchantId(orderId, merchant.id()));
    }

    @PutMapping("/{onlineName}/orders")
    public FullOrderDto createOrUpdateOrder(
        @PathVariable String onlineName,
        @RequestBody @Valid FullOrderDto orderDto
    ) {
        return new FullOrderDto(this.orderService.createFromCatalogOnline(orderDto, orderDto.merchantId()));
    }

    @PostMapping("/{onlineName}/distances")
    public RouteDto getDistances(
            @PathVariable String onlineName,
            @RequestBody @Valid AddressDto addressDto
    ) {
        var merchant = this.merchantRepository.findByOnlineName(onlineName)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Merchant not found"));

        var origin = new AddressDto(merchant.getAddress());

        RouteDto distance = logisticService.calculateDistance(origin, addressDto, merchant.getLogisticSetting());

        if (distance == null) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Erro ao calcular distância");
        }

        return distance;
    }
}
