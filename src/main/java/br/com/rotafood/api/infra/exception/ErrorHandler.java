package br.com.rotafood.api.infra.exception;

import jakarta.validation.ConstraintViolationException;
import jakarta.validation.ValidationException;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.List;

@RestControllerAdvice
public class ErrorHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<Object> handleError404(EntityNotFoundException ex) {
        return buildResponse(HttpStatus.NOT_FOUND, "Recurso não encontrado", ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Object> handleError400(MethodArgumentNotValidException ex) {
        List<DataErrorValidation> errors = ex.getFieldErrors()
                .stream()
                .map(error -> new DataErrorValidation(error.getField(), error.getDefaultMessage()))
                .toList();
        return buildResponse(HttpStatus.BAD_REQUEST, "Erro de validação nos campos", errors);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<Object> handleError400(HttpMessageNotReadableException ex) {
        return buildResponse(HttpStatus.BAD_REQUEST, "Erro no formato da requisição", ex.getMostSpecificCause().getMessage());
    }

    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<Object> handleErrorRegraDeNegocio(ValidationException ex) {
        return buildResponse(HttpStatus.BAD_REQUEST, "Erro de validação de negócio", ex.getMessage());
    }

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<Object> handleConstraintViolation(ConstraintViolationException ex) {
        List<DataErrorValidation> errors = ex.getConstraintViolations()
                .stream()
                .map(violation -> new DataErrorValidation(
                        violation.getPropertyPath().toString(),
                        violation.getMessage()
                )).toList();
        return buildResponse(HttpStatus.BAD_REQUEST, "Violação de restrição nos dados", errors);
    }

    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<Object> handleErrorBadCredentials(BadCredentialsException ex) {
        return buildResponse(HttpStatus.UNAUTHORIZED, "Credenciais inválidas", "Usuário ou senha incorretos.");
    }

    @ExceptionHandler(AuthenticationException.class)
    public ResponseEntity<Object> handleErrorAuth(AuthenticationException ex) {
        return buildResponse(HttpStatus.UNAUTHORIZED, "Falha na autenticação", ex.getMessage());
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<Object> handleErrorNotAllowed(AccessDeniedException ex) {
        return buildResponse(HttpStatus.FORBIDDEN, "Acesso negado", "Você não tem permissão para acessar este recurso.");
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Object> handleError500(Exception ex) {
        return buildResponse(HttpStatus.INTERNAL_SERVER_ERROR, "Erro interno no servidor", "Erro inesperado: " + ex.getLocalizedMessage());
    }

    private ResponseEntity<Object> buildResponse(HttpStatus status, String message, Object details) {
        return ResponseEntity.status(status).body(new ErrorResponse(
                status.value(),
                message,
                details,
                Instant.now()
        ));
    }

    public record DataErrorValidation(String field, String message) {
        public DataErrorValidation(FieldError erro) {
            this(erro.getField(), erro.getDefaultMessage());
        }
    }

    public record ErrorResponse(int status, String message, Object details, Instant timestamp) {
    }
}
