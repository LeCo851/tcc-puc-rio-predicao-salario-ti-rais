package br.com.leandrocoelho.springapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data // Gera Getters, Setters, toString, etc.
@AllArgsConstructor
@NoArgsConstructor
public class ResponsePrevisaoSalarioDTO {

    @JsonProperty("resultado")
    private ResultadoDTO resultado;

    @JsonProperty("status")
    private String status;

    // --- CLASSES INTERNAS (TAMBÉM DEVEM SER CLASSES) ---

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class ResultadoDTO {
        @JsonProperty("cargo_selecionado")
        private String cargoSelecionado;

        @JsonProperty("salario_estimado")
        private String salarioEstimado;

        // Este campo será preenchido pelo Java depois
        @JsonProperty("salario_corrigido")
        private String salarioCorrigido;

        @JsonProperty("fator_correcao")
        private java.math.BigDecimal fatorCorrecao;

        @JsonProperty("detalhes_perfil")
        private DetalhesPerfilDTO detalhesPerfil;
    }

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class DetalhesPerfilDTO {
        @JsonProperty("porte_empresa")
        private String porteEmpresa;

        @JsonProperty("setor_atuacao")
        private String setorAtuacao;
    }
}