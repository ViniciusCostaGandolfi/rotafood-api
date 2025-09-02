package br.com.rotafood.api.modules.common.application.controller.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import br.com.rotafood.api.modules.common.application.dto.WhatsAppWebhookRequest;
import br.com.rotafood.api.modules.common.application.service.WhatsAppWebhookService;
import io.swagger.v3.oas.annotations.parameters.RequestBody;
import jakarta.validation.Valid;

@RestController
@RequestMapping(ApiVersion.VERSION + "/webhook/whatsapp")
@Validated
public class WhatsAppWebhookController {

    @Autowired
    private WhatsAppWebhookService whatsAppWebhookService;


    @PostMapping
    public ResponseEntity<Void> post(
            @RequestBody @Valid WhatsAppWebhookRequest payload) {  
        System.err.println("\n\n"  + payload + "\n\n");
        return ResponseEntity.ok().build();
    }

    @GetMapping
    public ResponseEntity<String> get(
            @RequestParam("hub.mode") final String mode,
            @RequestParam("hub.challenge") final String challenge,
            @RequestParam("hub.verify_token") final String token) {

        this.whatsAppWebhookService.verifyWebhookToken(mode, token);

        System.out.println("Webhook verificado com sucesso!");
        return ResponseEntity.ok(challenge);
    }

}