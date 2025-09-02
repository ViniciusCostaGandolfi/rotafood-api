package br.com.rotafood.api.infra.security;

import java.io.IOException;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.annotation.Order;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import br.com.rotafood.api.modules.merchant.application.dto.MerchantUserDto;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component
@Order(2)
public class MerchantValidationFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(MerchantValidationFilter.class);
    private static final Pattern MERCHANT_ID_PATTERN = Pattern.compile(".*/merchants/([a-f0-9\\-]{36}).*");

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) 
            throws ServletException, IOException {

        String requestURI = request.getRequestURI();

        Matcher matcher = MERCHANT_ID_PATTERN.matcher(requestURI);
        if (matcher.matches()) {
            String merchantIdFromUrl = matcher.group(1);

            try {
                UUID merchantId = UUID.fromString(merchantIdFromUrl);
                var principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();

                if (principal instanceof MerchantUserDto merchantUserDto) {
                    if (!merchantUserDto.merchantId().equals(merchantId)) {
                        log.warn("Acesso negado: merchantId do usuário ({}) não bate com o merchantId da URL ({})",
                                merchantUserDto.merchantId(), merchantId);
                        response.setStatus(HttpServletResponse.SC_FORBIDDEN);
                        response.getWriter().write("Acesso negado");
                        return;
                    }
                } else {
                    response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                    return;
                }
            } catch (Exception e) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                response.getWriter().write("Merchant ID inválido ou request inválido.");
                return;
            }
        }

        filterChain.doFilter(request, response);
    }
}
