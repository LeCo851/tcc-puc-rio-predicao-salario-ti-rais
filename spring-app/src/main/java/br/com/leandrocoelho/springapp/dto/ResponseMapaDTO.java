package br.com.leandrocoelho.springapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.math.BigDecimal;

@Data
public class ResponseMapaDTO {
    private String uf;
    @JsonProperty("salario_estimado")
    private Double salarioEstimado;
    @JsonProperty("quantidade_total")
    private Integer quantidadeTotal;
    @JsonProperty("quantidade_masculino")
    private Integer quantidadeMasculino;
    @JsonProperty("quantidade_feminino")
    private Integer quantidadeFeminino;

    private String salarioCorrigido;
    private BigDecimal fatorCorrecao;
    private String salarioEstimadoFormatado;
}
