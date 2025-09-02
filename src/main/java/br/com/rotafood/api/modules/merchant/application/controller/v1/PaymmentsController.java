package br.com.rotafood.api.modules.merchant.application.controller.v1;

import java.util.NoSuchElementException;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import com.stripe.exception.StripeException;

import br.com.rotafood.api.infra.security.MerchantRoleAllowed;
import br.com.rotafood.api.modules.merchant.application.dto.StripePaymentStatusDto;
import br.com.rotafood.api.modules.merchant.application.service.StripePaymentService;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;

@RestController
@RequestMapping(ApiVersion.VERSION + "/merchants/{merchantId}")
public class PaymmentsController {

    @Autowired
    private StripePaymentService stripePaymentService;

    @MerchantRoleAllowed(MerchantUserRole.OWNER)
    @GetMapping("/payments")
    public ResponseEntity<StripePaymentStatusDto> listPayments(
            @PathVariable UUID merchantId,
            @RequestParam(name = "session_id", required = false) String sessionId) {
        try {
            StripePaymentStatusDto response = stripePaymentService.validateAndFetchStripeData(merchantId, sessionId);
            return ResponseEntity.ok(response);
        } catch (StripeException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Erro ao acessar Stripe", e);
        }
    }

    @MerchantRoleAllowed(MerchantUserRole.OWNER)
    @PostMapping("/payments/cancel-subscription")
    public ResponseEntity<StripePaymentStatusDto> cancelSubscription(
            @PathVariable UUID merchantId,
            @RequestParam String subscriptionId
            ) {
        try {
            StripePaymentStatusDto canceledStatus =
                    stripePaymentService.cancelSubscription(merchantId, subscriptionId);
            return ResponseEntity.ok(canceledStatus);
        } catch (StripeException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Erro ao acessar Stripe", e);
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, e.getMessage(), e);
        } catch (NoSuchElementException e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, e.getMessage(), e);
        }
    }
}

