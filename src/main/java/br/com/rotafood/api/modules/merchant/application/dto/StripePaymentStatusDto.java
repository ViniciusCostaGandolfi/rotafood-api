package br.com.rotafood.api.modules.merchant.application.dto;

import java.util.List;

public record StripePaymentStatusDto(
    boolean active,
    String message,
    String email,
    int totalSubscriptions,
    List<StripeSubscriptionDto> subscriptions,
    List<StripeChargeDto> payments
) {}
