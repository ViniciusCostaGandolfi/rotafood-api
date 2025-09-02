package br.com.rotafood.api.modules.common.application.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;

@Service
public class WhatsAppWebhookService {

    @Value("${whatsapp.token}")
    private String verifyToken;


    public void verifyWebhookToken(String mode, String token) {
        if (!"subscribe".equals(mode) || !this.verifyToken.equals(token)) {
            throw new AccessDeniedException("Token de verificação do Webhook inválido.");
        }
    }
}
