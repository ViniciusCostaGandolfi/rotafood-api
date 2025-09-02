package br.com.rotafood.api.modules.order.application.controller.v1;


import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import br.com.rotafood.api.modules.order.application.dto.CommandDto;
import br.com.rotafood.api.modules.order.application.dto.FullCommandDto;
import br.com.rotafood.api.modules.order.application.service.CommandService;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping(ApiVersion.VERSION + "/merchants/{merchantId}/commands")
public class CommandController {

    @Autowired
    private CommandService commandService;

    @GetMapping
    public List<FullCommandDto> getAll(
        @PathVariable UUID merchantId
    ) {
        return commandService.getAllByMerchantId(merchantId)
                .stream()
                .map(FullCommandDto::new)
                .toList();
    }

    @GetMapping("/simplified")
    public List<CommandDto> getAllSimplified(
        @PathVariable UUID merchantId
    ) {

        return commandService.getAllByMerchantId(merchantId)
                .stream()
                .map(CommandDto::new)
                .toList();
    }

    @GetMapping("/{commandId}")
    public FullCommandDto getById(
        @PathVariable UUID merchantId,
        @PathVariable UUID commandId
    ) {
        return new FullCommandDto(commandService.getByIdAndMerchantId(commandId, merchantId));
    }

    @PutMapping
    public FullCommandDto createOrUpdate(
        @PathVariable UUID merchantId,
        @RequestBody @Valid FullCommandDto commandDto
    ) {
        return new FullCommandDto(commandService.createOrUpdate(commandDto, merchantId));
    }

    @PutMapping("/{commandId}/close")
    public void closeCommand(
        @PathVariable UUID merchantId,
        @PathVariable UUID commandId,
        @RequestBody @Valid FullCommandDto commandDto

    ) {
        commandService.closeCommand(commandDto, merchantId);
    }

    @DeleteMapping("/{commandId}")
    public void deleteCommand(
        @PathVariable UUID merchantId,
        @PathVariable UUID commandId
    ) {
        commandService.deleteByIdAndMerchantId(commandId, merchantId);
    }
}
