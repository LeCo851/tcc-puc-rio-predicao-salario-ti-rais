package br.com.leandrocoelho.springapp.service;

import br.com.leandrocoelho.springapp.dto.DadosProfissionalDTO;
import br.com.leandrocoelho.springapp.dto.PrevisaoSalarioDTO;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class SalarioService {

    @Value("${ml.api.url}") //ler url do app properties
    private String mlApiUrl;

    private final RestTemplate restTemplate;

    public PrevisaoSalarioDTO obterEstimativa(DadosProfissionalDTO dados) {
        long inicio = System.currentTimeMillis();
        System.out.println(">>> [JAVA] Iniciando chamada ao Python...");

        try {
            PrevisaoSalarioDTO resposta = restTemplate.postForObject(
                    mlApiUrl,
                    dados,
                    PrevisaoSalarioDTO.class
            );

            long fim = System.currentTimeMillis();
            System.out.println(">>> [JAVA] Resposta recebida em: " + (fim - inicio) + " ms");

            return resposta;
        } catch (Exception e) {
            long fim = System.currentTimeMillis();
            System.out.println(">>> [JAVA] Erro após: " + (fim - inicio) + " ms");
            throw e;
        }
    }
}
