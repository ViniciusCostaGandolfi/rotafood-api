package br.com.rotafood.api.infra.config;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;

@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate(ObjectMapper objectMapper) {
        RestTemplate restTemplate = new RestTemplate();

        restTemplate.getMessageConverters().removeIf(converter -> converter instanceof org.springframework.http.converter.xml.MappingJackson2XmlHttpMessageConverter);
        
        restTemplate.getMessageConverters().add(new MappingJackson2HttpMessageConverter(objectMapper));

        return restTemplate;
    }

}