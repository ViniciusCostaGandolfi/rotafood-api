package br.com.rotafood.api.modules.order.application.dto;

import java.util.UUID;

import br.com.rotafood.api.modules.order.domain.entity.Command;

public record CommandDto(
    UUID id,
    String name,
    Integer merchantSequence,
    Integer tableIndex
) {

    public CommandDto(Command command) {
        this(
            command.getId(), 
            command.getName(), 
            command.getMerchantSequence(), 
            command.getTableIndex());
    }
    
}
