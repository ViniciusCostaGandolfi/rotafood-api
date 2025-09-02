package br.com.rotafood.api.modules.merchant.application.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.stripe.exception.StripeException;
import com.stripe.model.Charge;
import com.stripe.model.ChargeCollection;
import com.stripe.model.Customer;
import com.stripe.model.CustomerCollection;
import com.stripe.model.Subscription;
import com.stripe.model.SubscriptionCollection;
import com.stripe.model.checkout.Session;

import br.com.rotafood.api.modules.merchant.application.dto.StripeChargeDto;
import br.com.rotafood.api.modules.merchant.application.dto.StripePaymentStatusDto;
import br.com.rotafood.api.modules.merchant.application.dto.StripeSubscriptionDto;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;

@Service
public class StripePaymentService {

    @Autowired
    private MerchantRepository merchantRepository;


    public StripePaymentStatusDto validateAndFetchStripeData(UUID merchantId, String sessionId) throws StripeException {
        Merchant merchant = merchantRepository.findById(merchantId)
                .orElseThrow(() -> new NoSuchElementException("Merchant não encontrado"));

        updateMerchantWithSessionInfoIfComplete(merchant, sessionId);

        String customerId = findOrCreateStripeCustomerIfNecessary(merchant);

        if (customerId == null) {
            return new StripePaymentStatusDto(
                    false,
                    "Cliente não encontrado no Stripe",
                    null,
                    0,
                    List.of(),
                    List.of()
            );
        }

        List<StripeSubscriptionDto> subscriptions = fetchCustomerSubscriptions(customerId);
        List<StripeChargeDto> payments = fetchCustomerCharges(customerId);

        boolean isActive = subscriptions.stream()
                .anyMatch(s -> "active".equalsIgnoreCase(s.status()));

        return new StripePaymentStatusDto(
                isActive,
                isActive ? "Assinatura ativa encontrada" : "Nenhuma assinatura ativa",
                merchant.getOwnerEmail(),
                subscriptions.size(),
                subscriptions,
                payments
        );
    }


    private void updateMerchantWithSessionInfoIfComplete(Merchant merchant, String sessionId) throws StripeException {
        if (sessionId == null) {
            return;
        }
        Session session = Session.retrieve(sessionId);
        if ("complete".equals(session.getStatus())) {
            merchant.setStripeSessionId(session.getId());
            merchant.setStripeCustomerId(session.getCustomer());
            merchant.setStripeSubscriptionId(session.getSubscription());
            merchant.setIsSubscriptionActive(true);
            merchantRepository.save(merchant);
        }
    }


    private String findOrCreateStripeCustomerIfNecessary(Merchant merchant) throws StripeException {
        String customerId = merchant.getStripeCustomerId();

        if (customerId == null) {
            Map<String, Object> params = Map.of("email", merchant.getOwnerEmail());
            CustomerCollection customers = Customer.list(params);

            if (!customers.getData().isEmpty()) {
                customerId = customers.getData().get(0).getId();
                merchant.setStripeCustomerId(customerId);
                merchantRepository.save(merchant);
            }
        }
        return customerId;
    }


    private List<StripeSubscriptionDto> fetchCustomerSubscriptions(String customerId) throws StripeException {
        SubscriptionCollection subscriptionCollection = Subscription.list(Map.of("customer", customerId));
        List<StripeSubscriptionDto> subscriptions = new ArrayList<>();
    
        for (Subscription sub : subscriptionCollection.getData()) {
            Instant startDate = (sub.getStartDate() != null)
                    ? Instant.ofEpochSecond(sub.getStartDate())
                    : null;
    
            Instant endedAt = (sub.getEndedAt() != null)
                    ? Instant.ofEpochSecond(sub.getEndedAt())
                    : null;
    
            subscriptions.add(
                new StripeSubscriptionDto(
                    sub.getId(),       
                    sub.getStatus(),   
                    startDate,
                    endedAt
                )
            );
        }
    
        return subscriptions;
    }
    


    private List<StripeChargeDto> fetchCustomerCharges(String customerId) throws StripeException {
        ChargeCollection chargeCollection = Charge.list(Map.of("customer", customerId));
        List<StripeChargeDto> payments = new ArrayList<>();

        for (Charge c : chargeCollection.getData()) {
            BigDecimal amountDecimal = BigDecimal.valueOf(c.getAmount())
                    .divide(BigDecimal.valueOf(100));

            Instant created = Instant.ofEpochSecond(c.getCreated());

            payments.add(
                    new StripeChargeDto(
                            c.getId(),
                            amountDecimal,
                            created,
                            c.getCurrency()
                    )
            );
        }
        return payments;
    }

    public StripePaymentStatusDto cancelSubscription(UUID merchantId, String subscriptionId) throws StripeException {
        Merchant merchant = merchantRepository.findById(merchantId)
            .orElseThrow(() -> new NoSuchElementException("Merchant não encontrado"));

        Subscription subscription = Subscription.retrieve(subscriptionId);

        if (!subscription.getCustomer().equals(merchant.getStripeCustomerId())) {
            throw new IllegalArgumentException("A assinatura não pertence ao Merchant informado.");
        }

        subscription.cancel();


        merchant.setIsSubscriptionActive(false);
        merchantRepository.save(merchant);


        return validateAndFetchStripeData(merchantId, null);
    }
}
