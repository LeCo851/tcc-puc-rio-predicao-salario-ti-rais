package br.com.leandrocoelho.springapp.service;

import br.com.leandrocoelho.springapp.dto.DadosProfissionalDTO;
import br.com.leandrocoelho.springapp.dto.ResponsePrevisaoSalarioDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
@Slf4j
public class SalarioService {

    @Value("${ml.api.url}") //ler url do app properties
    private String mlApiUrl;

    private final RestTemplate restTemplate;
    private final CorrecaoMonetariaService correcaoMonetariaService;

    public ResponsePrevisaoSalarioDTO obterEstimativa(DadosProfissionalDTO dados) {
        long inicio = System.currentTimeMillis();
        log.info(">>> [JAVA] Iniciando chamada ao Python para o cargo: {}",dados.getCargo());

        try {
            ResponsePrevisaoSalarioDTO resposta = restTemplate.postForObject(
                    mlApiUrl,
                    dados,
                    ResponsePrevisaoSalarioDTO.class
            );
            if(resposta != null){
                correcaoMonetariaService.aplicarCorrecao(resposta,dados.getAnoReferencia());
                // Log opcional para ver se funcionou
                log.info(">>> Correção aplicada. Valor Original: {} | Ajustado: {}",
                        resposta.getResultado().getSalarioEstimado(),
                        resposta.getResultado().getSalarioCorrigido());
            }

            long tempoTotal = System.currentTimeMillis() - inicio;
            log.info(">>> Sucesso! Resposta recebidae e processada em {} ms",tempoTotal);

            return resposta;
        } catch (Exception e) {
            long tempoTotal = System.currentTimeMillis() - inicio;
            log.error(">>> Erro na comunicação com IA após {} ms. Causa: {}", tempoTotal, e.getMessage());
            throw e;
        }
    }
}
