package br.com.leandrocoelho.springapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record PrevisaoSalarioDTO(
        @JsonProperty("resultado") ResultadoDTO resultado,
        @JsonProperty("status") String status

) {
    public record ResultadoDTO(
            @JsonProperty("cargo_selecionado")
            String cargoSelecionado,

            @JsonProperty("salario_estimado")
            String salarioEstimado,

            @JsonProperty("detalhes_perfil")
            DetalhesPerfilDTO detalhesPerfil

    ){}

    public record DetalhesPerfilDTO(
            @JsonProperty("porte_empresa")
            String porteEmpresa,
            @JsonProperty("setor_atuacao")
            String setorAtuacao
    ){}
}
