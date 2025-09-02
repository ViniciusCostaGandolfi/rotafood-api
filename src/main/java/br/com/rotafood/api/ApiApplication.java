package br.com.rotafood.api;

import java.io.IOException;
import java.net.URISyntaxException;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;


@EnableAspectJAutoProxy
@SpringBootApplication
@EnableAsync
@EnableScheduling
public class ApiApplication {

    public static void main(String[] args) throws IOException, URISyntaxException {
        SpringApplication.run(ApiApplication.class, args);
        System.out.println("\n\n\n Aplica\u00e7\u00e3o dispon\u00edvel em: \u001b[34m http://localhost:8080/swagger-ui.html \u001b[0m");
    }
}
