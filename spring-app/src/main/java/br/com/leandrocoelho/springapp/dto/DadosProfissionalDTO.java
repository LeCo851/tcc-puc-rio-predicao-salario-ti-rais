package br.com.leandrocoelho.springapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record DadosProfissionalDTO(
        String cargo,
        Integer idade,
        String escolaridade,
        String uf,
        String sexo,
        String raca,
        @JsonProperty("tamanho_empresa")
        String tamanhoEmpresa,
        @JsonProperty("setor")
        String setor,
        @JsonProperty("ano_referencia")
        Integer anoReferencia
) {}
