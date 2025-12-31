package br.com.leandrocoelho.springapp.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data // Gera Getters, Setters, toString, etc.
@AllArgsConstructor
@NoArgsConstructor
@Builder
@JsonIgnoreProperties(ignoreUnknown = true)
public class ResponsePrevisaoSalarioDTO {

    @JsonProperty("resultado")
    private ResultadoDTO resultado;

    @JsonProperty("mensagem")
    private String status;
    @JsonProperty("cargo")
    private String cargoSelecionado;

    // --- CLASSES INTERNAS (TAMBÉM DEVEM SER CLASSES) ---

    @Data
    @Builder
    @AllArgsConstructor
    @NoArgsConstructor
    public static class ResultadoDTO {


        @JsonProperty("salario_estimado")
        private Double salarioEstimado;

        // Este campo será preenchido pelo Java depois
        @JsonProperty("salario_corrigido")
        private String salarioCorrigido;

        @JsonProperty("fator_correcao")
        private java.math.BigDecimal fatorCorrecao;


        @JsonProperty("faixa_confianca_min")
        private Double faixaConfiancaMin;
        @JsonProperty("faixa_confianca_max")
        private Double faixaConfiancaMax;

        private String salarioMinFormatado; // faixa minima do salario que é devolvido ao front
        private String salarioMaxFormatado; // faixa maxima do salario que é devolvido ao front
        private DetalhesPerfilDTO detalhesPerfil;
    }
    @Data
    @Builder
    @AllArgsConstructor
    @NoArgsConstructor
    public static class DetalhesPerfilDTO {
        private String porteEmpresa;
        private String escolaridade;
        private String nivelExperiencia; // Para mostrar se foi JUNIOR/PLENO...
    }
}