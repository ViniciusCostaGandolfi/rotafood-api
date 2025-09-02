package br.com.rotafood.api.modules.logistic.application.controller.v1;

import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.rotafood.api.modules.logistic.application.dto.VrpOutDto;
import br.com.rotafood.api.modules.order.application.service.OrderVrpService;

@RestController
@RequestMapping( ApiVersion.VERSION + "/merchants/merchantId/vrp")
public class VrpController {

    @Autowired
    private OrderVrpService orderVrpService; 


    @PostMapping
    public ResponseEntity<VrpOutDto> roteirizarPedidosDelivery(
            @PathVariable UUID merchantId
    ) {
        VrpOutDto vrpOut = orderVrpService.generateDeliveryRoutes(merchantId);
        return ResponseEntity.ok(vrpOut);
    }
    
}
