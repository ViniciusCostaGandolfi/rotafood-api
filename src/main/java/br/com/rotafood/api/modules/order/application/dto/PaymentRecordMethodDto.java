package br.com.rotafood.api.modules.order.application.dto;

import java.math.BigDecimal;
import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.PaymentRecordMethod;
import br.com.rotafood.api.modules.order.domain.entity.PaymentRecordMethodType;
import br.com.rotafood.api.modules.order.domain.entity.PaymentRecordType;
import jakarta.validation.constraints.NotNull;

public record PaymentRecordMethodDto(
    UUID id,
    String description,
    @NotNull
    PaymentRecordMethodType method,
    @NotNull
    boolean paid,
    PaymentRecordType type,
    BigDecimal value,
    BigDecimal changeFor
) {
    public PaymentRecordMethodDto(PaymentRecordMethod method) {
    this(
        method.getId(),
        method.getDescription(),
        method.getMethod(),
        method.isPaid(),
        method.getType(),
        method.getValue(),
        method.getChangeFor()
    );
}

}
