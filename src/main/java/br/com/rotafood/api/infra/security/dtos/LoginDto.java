package br.com.rotafood.api.infra.security.dtos;

public record LoginDto (
    String email,
    String password
) {}
