package br.com.leandrocoelho.springapp.exceptions;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;

import java.time.Instant;

@ControllerAdvice
public class ExceptionHandlerController {

    @ExceptionHandler(HttpClientErrorException.class)
    public ResponseEntity<StandardError> pythonError( HttpClientErrorException e, HttpServletRequest request){
        String error = "Erro ao inferir o resultado";
        HttpStatus status = (HttpStatus) e.getStatusCode();

        String msgAmigavel = "Os dados enviados foram rejeitados pelo modelo";

        StandardError err = new StandardError(
                Instant.now(),
                status.value(),
                error,
                msgAmigavel,
                request.getRequestURI()
        );
        return ResponseEntity.status(status).body(err);
    }

    // 2. Trata erro de conexão (Python desligado / Docker caiu)
    @ExceptionHandler(ResourceAccessException.class)
    public ResponseEntity<StandardError> connectionError(ResourceAccessException e, HttpServletRequest request) {
        String error = "Erro de Conexão";
        HttpStatus status = HttpStatus.SERVICE_UNAVAILABLE; // 503
        String msg = "Não foi possível conectar ao serviço de IA. O container Python está rodando?";

        StandardError err = new StandardError(Instant.now(), status.value(), error, msg, request.getRequestURI());
        return ResponseEntity.status(status).body(err);
    }

    // 3. Trata qualquer outro erro genérico (NullPointer, etc)
    @ExceptionHandler(Exception.class)
    public ResponseEntity<StandardError> genericError(Exception e, HttpServletRequest request) {
        String error = "Erro Interno do Servidor";
        HttpStatus status = HttpStatus.INTERNAL_SERVER_ERROR; // 500
        String msg = "Ocorreu um erro inesperado: " + e.getMessage();

        StandardError err = new StandardError(Instant.now(), status.value(), error, msg, request.getRequestURI());
        return ResponseEntity.status(status).body(err);
    }
    // Trata erros de validação de negócio ou dados nulos enviados pelo usuário
    @ExceptionHandler(DadosInvalidosException.class)
    public ResponseEntity<StandardError> businessError(DadosInvalidosException e, HttpServletRequest request) {
        String error = "Requisição Inválida";
        HttpStatus status = HttpStatus.BAD_REQUEST; // Código 400

        String msgAmigavel = "Certifique-se de que todos os campos obrigatórios (Cargo, Ano, Idade,...) foram preenchidos corretamente.";

        StandardError err = new StandardError(
                Instant.now(),
                status.value(),
                error,
                msgAmigavel, // Aqui virá a mensagem que você escreveu no 'throw'
                request.getRequestURI()
        );
        return ResponseEntity.status(status).body(err);
    }

}
