package br.com.leandrocoelho.springapp.service;

import br.com.leandrocoelho.springapp.dto.ResponseMapaDTO;
import br.com.leandrocoelho.springapp.dto.ResponsePrevisaoSalarioDTO;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.text.NumberFormat;
import java.util.Locale;

@Service
public class CorrecaoMonetariaService {

    // --- MÉTODOS PÚBLICOS (ADAPTADORES) ---

    // Caso 1: Previsão Única (Recebe String formatada "R$ 1.000,00")
    public void aplicarCorrecao(ResponsePrevisaoSalarioDTO dto, int anoReferencia) {
        if (dto == null || dto.getResultado() == null) return;

        var resultadoObj = dto.getResultado();
        try {
            // Converte a String "R$ X" para BigDecimal
            BigDecimal valorOriginal = BigDecimal.valueOf(resultadoObj.getSalarioEstimado());

            // Chama a lógica centralizada
            ResultadoCorrecao salarioCorrigido = calcularCorrecao(valorOriginal, anoReferencia);

            // Aplica os valores de volta
            resultadoObj.setFatorCorrecao(salarioCorrigido.fator());
            resultadoObj.setSalarioCorrigido(salarioCorrigido.valorFormatado());

            if(resultadoObj.getFaixaConfiancaMin() != null){
                BigDecimal valorMin = BigDecimal.valueOf(resultadoObj.getFaixaConfiancaMin());
                ResultadoCorrecao resMin = calcularCorrecao(valorMin,anoReferencia);
                resultadoObj.setSalarioMinFormatado(resMin.valorFormatado());
            }

            if(resultadoObj.getFaixaConfiancaMax() != null){
                BigDecimal valorMax = BigDecimal.valueOf(resultadoObj.getFaixaConfiancaMax());
                ResultadoCorrecao resMax = calcularCorrecao(valorMax,anoReferencia);
                resultadoObj.setSalarioMaxFormatado(resMax.valorFormatado());
            }

        } catch (Exception e) {
            // Fallback em caso de erro
            BigDecimal salarioOriginal = BigDecimal.valueOf(resultadoObj.getSalarioEstimado());
            resultadoObj.setFatorCorrecao(BigDecimal.ONE);
            resultadoObj.setSalarioCorrigido(formatarMoeda(salarioOriginal));
            resultadoObj.setSalarioMinFormatado(null);
            resultadoObj.setSalarioMaxFormatado(null);

        }
    }

    // Caso 2: Mapa (Recebe Double puro do Python ex: 1000.0)
    public void aplicarCorrecaoMapa(ResponseMapaDTO item, int anoReferencia) {
        if (item == null || item.getSalarioEstimado() == null) return;

        try {
            // Conversão direta de Double para BigDecimal (MUITO MAIS SEGURO)
            BigDecimal valorOriginal = BigDecimal.valueOf(item.getSalarioEstimado());

            // Reusa a MESMA lógica centralizada
            ResultadoCorrecao resultado = calcularCorrecao(valorOriginal, anoReferencia);

            // Aplica os valores
            item.setFatorCorrecao(resultado.fator());
            item.setSalarioCorrigido(resultado.valorFormatado());
            item.setSalarioEstimadoFormatado(formatarMoeda(BigDecimal.valueOf(item.getSalarioEstimado())));

        } catch (Exception e) {
            // Fallback
            item.setFatorCorrecao(BigDecimal.ONE);
            item.setSalarioCorrigido(formatarMoeda(BigDecimal.valueOf(item.getSalarioEstimado())));
        }
    }

    // --- LÓGICA DE NEGÓCIO CENTRALIZADA (CORE) ---

    // Record auxiliar interno para transportar o resultado
    private record ResultadoCorrecao(BigDecimal fator, String valorFormatado) {}

    private ResultadoCorrecao calcularCorrecao(BigDecimal valorOriginal, int ano) {
        BigDecimal fator = obterFatorIPCA(ano);
        BigDecimal valorCorrigido = valorOriginal.multiply(fator);
        String formatado = formatarMoeda(valorCorrigido);

        return new ResultadoCorrecao(fator, formatado);
    }

    // --- MÉTODOS AUXILIARES ---

    private BigDecimal obterFatorIPCA(int anoReferencia) {
        return switch (anoReferencia) {
            case 2019 -> new BigDecimal("1.4250");
            case 2020 -> new BigDecimal("1.3660");
            case 2021 -> new BigDecimal("1.2950");
            case 2022 -> new BigDecimal("1.1730");
            case 2023 -> new BigDecimal("1.1090");
            case 2024 -> new BigDecimal("1.0450");
            default -> BigDecimal.ONE;
        };
    }

    private String formatarMoeda(BigDecimal valor) {
        return NumberFormat.getCurrencyInstance(Locale.forLanguageTag("pt-BR")).format(valor);
    }

}