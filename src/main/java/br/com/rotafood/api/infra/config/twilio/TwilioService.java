package br.com.rotafood.api.infra.config.twilio;

import com.twilio.Twilio;
import com.twilio.type.PhoneNumber;
import com.twilio.rest.api.v2010.account.Message;

import java.util.HashMap;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class TwilioService {

    @Value("${TWILIO_ACCOUNT_SID}")
    private String accountSid;

    @Value("${TWILIO_AUTH_TOKEN}")
    private String authToken;

    @Value("${TWILIO_PHONE_NUMBER}")
    private String twilioPhoneNumber;

    public void sendSms(String toPhoneNumber, String messageBody) {
        Twilio.init(accountSid, authToken);

        Message message = Message.creator(
                new PhoneNumber(toPhoneNumber),
                new PhoneNumber(twilioPhoneNumber),
                messageBody 
        ).create();

        System.out.println("SMS enviado com sucesso: " + message.getSid());
    }


    public void sendWhatsApp(String toPhoneNumber, String messageBody) {
        Twilio.init(accountSid, authToken);
    
        Message message = Message.creator(
            new PhoneNumber("whatsapp:" + toPhoneNumber),
            new PhoneNumber("whatsapp:" + twilioPhoneNumber),
            messageBody
        )
        .setMessagingServiceSid("MG9dc628f78fcd67b236b854e0f307d320")
        .create();

        System.out.println(message.getBody());    
    }


    public void sendWhatsAppTemplate(String toPhoneNumber, String pedido, String restaurante, String url) {
        Twilio.init(accountSid, authToken);

        JSONObject contentVariables = new JSONObject(new HashMap<String, Object>() {{
            put("1", pedido);
            put("2", restaurante);
            put("3", url);
        }});

        Message message = Message.creator(
                new PhoneNumber("whatsapp:" + toPhoneNumber),
                new PhoneNumber("whatsapp:" + twilioPhoneNumber),
                (String) null 
            )
            .setMessagingServiceSid("MG9dc628f78fcd67b236b854e0f307d320") 
            .setContentSid("HX9fa7a06979e7fc72ccc8d2e4a40f8ebb") 
            .setContentVariables(contentVariables.toString())
            .create();

        System.out.println("Mensagem de template enviada: " + message.getSid());
    }
        
}
