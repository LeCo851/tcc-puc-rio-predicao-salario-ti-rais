package br.com.leandrocoelho.springapp.exceptions;

public class DadosInvalidosException extends RuntimeException {
    public DadosInvalidosException(String message) {
        super(message);
    }
}
