package br.com.rotafood.api.modules.merchant.application.dto;

import java.math.BigDecimal;
import java.time.Instant;

public record StripeChargeDto(
    String id,
    BigDecimal amount,
    Instant created,
    String currency
) {}
