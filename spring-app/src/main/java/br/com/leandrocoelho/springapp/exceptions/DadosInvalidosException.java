package br.com.leandrocoelho.springapp.exceptions;

public class DadosInvalidosException extends RuntimeException {
    public DadosInvalidosException() {
        super("Dados inválidos");
    }
}
