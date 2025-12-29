package br.com.leandrocoelho.springapp.service;

import br.com.leandrocoelho.springapp.dto.PrevisaoSalarioDTO;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.text.NumberFormat;
import java.util.Locale;

@Service
public class CorrecaoMonetariaService {

    public void aplicarCorrecao(PrevisaoSalarioDTO previsaoSalarioDTO, int anoReferencia){
        if(previsaoSalarioDTO == null || previsaoSalarioDTO.getResultado() == null) return;

        try{
            String salarioString = previsaoSalarioDTO.getResultado().getSalarioEstimado();
            BigDecimal valorOriginal = converterStringParaDecimal(salarioString);

            BigDecimal fatorInflacao = obterFatorIPCA(anoReferencia);

            BigDecimal valorCorrigido = valorOriginal.multiply(fatorInflacao);

            previsaoSalarioDTO.getResultado().setFatorCorrecao(fatorInflacao);

            String salarioCorrigidoStr = formatarMoeda(valorCorrigido);

            previsaoSalarioDTO.getResultado().setSalarioCorrigido(salarioCorrigidoStr);
        }catch (Exception e){
            previsaoSalarioDTO.getResultado().setSalarioEstimado(previsaoSalarioDTO.getResultado().getSalarioEstimado());
            previsaoSalarioDTO.getResultado().setFatorCorrecao(BigDecimal.ONE);

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
