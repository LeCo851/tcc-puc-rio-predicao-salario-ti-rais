package br.com.leandrocoelho.springapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class DadosProfissionalDTO{

    private String cargo;
    private Integer idade;
    private String escolaridade;
    private String uf;
    private String sexo;
    private String raca;
    @JsonProperty("tamanho_empresa")
    private String tamanhoEmpresa;
    @JsonProperty("setor")
    private String setor;
    @JsonProperty(value = "ano_referencia",required = true)
    private Integer anoReferencia;
}
