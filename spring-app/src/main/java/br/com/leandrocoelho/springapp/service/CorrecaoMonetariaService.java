package br.com.leandrocoelho.springapp.service;

import br.com.leandrocoelho.springapp.dto.ResponseMapaDTO;
import br.com.leandrocoelho.springapp.dto.ResponsePrevisaoSalarioDTO;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.text.NumberFormat;
import java.util.Locale;

@Service
public class CorrecaoMonetariaService {

    public void aplicarCorrecao(ResponsePrevisaoSalarioDTO responsePrevisaoSalarioDTO, int anoReferencia){
        if(responsePrevisaoSalarioDTO == null || responsePrevisaoSalarioDTO.getResultado() == null) return;

        try{
            String salarioString = responsePrevisaoSalarioDTO.getResultado().getSalarioEstimado();
            BigDecimal valorOriginal = converterStringParaDecimal(salarioString);

            BigDecimal fatorInflacao = obterFatorIPCA(anoReferencia);

            BigDecimal valorCorrigido = valorOriginal.multiply(fatorInflacao);

            responsePrevisaoSalarioDTO.getResultado().setFatorCorrecao(fatorInflacao);

            String salarioCorrigidoStr = formatarMoeda(valorCorrigido);

            responsePrevisaoSalarioDTO.getResultado().setSalarioCorrigido(salarioCorrigidoStr);
        }catch (Exception e){
            responsePrevisaoSalarioDTO.getResultado().setSalarioEstimado(responsePrevisaoSalarioDTO.getResultado().getSalarioEstimado());
            responsePrevisaoSalarioDTO.getResultado().setFatorCorrecao(BigDecimal.ONE);

        }

    }

    public void aplicarCorrecaoMapa(ResponseMapaDTO item, int anoReferencia) {
        if (item == null || item.getSalarioEstimado() == null) return;

        try {
            // No mapa, o salário já vem como Double, facilitando a vida
            BigDecimal valorOriginal = BigDecimal.valueOf(item.getSalarioEstimado());

            BigDecimal fatorInflacao = obterFatorIPCA(anoReferencia);
            BigDecimal valorCorrigido = valorOriginal.multiply(fatorInflacao);

            // Setamos os valores no DTO do mapa (certifique-se de que o DTO tenha esses campos)
            item.setFatorCorrecao(fatorInflacao);
            item.setSalarioCorrigido(formatarMoeda(valorCorrigido));

        } catch (Exception e) {
            item.setSalarioCorrigido(formatarMoeda(BigDecimal.valueOf(item.getSalarioEstimado())));
            item.setFatorCorrecao(BigDecimal.ONE);
        }
    }

    private String formatarMoeda(BigDecimal valorCorrigido) {
        NumberFormat nf = NumberFormat.getCurrencyInstance(Locale.forLanguageTag("pt-BR"));
        return nf.format(valorCorrigido);
    }

    private BigDecimal obterFatorIPCA(int anoReferencia) {
        return switch (anoReferencia){
            case 2019 -> new BigDecimal("1.4250");
            case 2020 -> new BigDecimal("1.3660");
            case 2021 -> new BigDecimal("1.2950");
            case 2022 -> new BigDecimal("1.1730");
            case 2023 -> new BigDecimal("1.1090");
            case 2024 -> new BigDecimal("1.0450");
            default -> BigDecimal.ONE;
        };
    }

    private BigDecimal converterStringParaDecimal(String salarioString) {
        String limpo = salarioString.replaceAll("[^0-9,]", "").replace(",", ".");
        return new BigDecimal(limpo);
    }
}
