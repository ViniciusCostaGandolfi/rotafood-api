package br.com.rotafood.api.infra.security;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTCreationException;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference; 
import com.fasterxml.jackson.databind.ObjectMapper;

import br.com.rotafood.api.infra.security.dtos.TokenJwtDto;
import br.com.rotafood.api.modules.merchant.application.dto.MerchantUserDto;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUser;

@Service 
public class TokenService {

    @Value("${api.security.token.secret}")
    private String secret;

    @Autowired
    ObjectMapper objectMapper;


    public TokenJwtDto generateToken(MerchantUser merchantUser) throws JsonProcessingException {
        try {
            var algorithm = Algorithm.HMAC256(secret);
            var expirationTime = this.expiration();
            var merchantUserDto = new MerchantUserDto(merchantUser);
            var json = objectMapper.writeValueAsString(merchantUserDto);
            Map<String, Object> map = objectMapper.readValue(json, new TypeReference<>() {});
            var tokenJwt = JWT.create()
            .withIssuer("API rotafood.com.br")
            .withClaim("merchantUser", map)
            .withExpiresAt(expirationTime)
            .sign(algorithm);
            
            return new TokenJwtDto(tokenJwt);
        } catch (JWTCreationException exception){
            throw new RuntimeException("Erro ao gerar token jwt", exception);
        }
    }

    public String getSubject(String tokenJWT) {
        try {
            var algorithm = Algorithm.HMAC256(secret);
            var token =  JWT.require(algorithm)
                    .withIssuer("API rotafood.com.br")
                    .build()
                    .verify(tokenJWT)
                    .getSubject();

            return token;
        } catch (JWTVerificationException exception) {
            throw new RuntimeException("Token JWT inválido ou expirado!");
        }
    }

    public MerchantUserDto getMerchantUser(String tokenJWT) {
        try {
            var algorithm = Algorithm.HMAC256(secret);
            var merchantUserClaim =  JWT.require(algorithm)
                    .withIssuer("API rotafood.com.br")
                    .build()
                    .verify(tokenJWT)
                    .getClaim("merchantUser")
                    .asMap();

            return objectMapper.convertValue(merchantUserClaim, MerchantUserDto.class);
        } catch (JWTVerificationException exception) {
            throw new RuntimeException("Token JWT inválido ou expirado!");
        }
    }

    
    private Instant expiration() {
        return LocalDateTime.now().plusDays(14).toInstant(ZoneOffset.of("-03:00"));
    }   
}