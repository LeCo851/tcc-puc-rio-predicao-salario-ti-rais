package br.com.leandrocoelho.springapp.service;

import br.com.leandrocoelho.springapp.dto.DadosProfissionalDTO;
import br.com.leandrocoelho.springapp.dto.ResponseMapaDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class MapaService {

    @Value("${ml.api.url.mapa}")
    private String mlApiUrlMapa;

    private final RestTemplate restTemplate;
    private final CorrecaoMonetariaService correcaoMonetariaService;

    public List<ResponseMapaDTO> obterDadosMapa(DadosProfissionalDTO dadosProfissionalDTO){

            ResponseMapaDTO[] resposta = restTemplate.postForObject(
                    mlApiUrlMapa,
                    dadosProfissionalDTO,
                    ResponseMapaDTO[].class
            );
            if(resposta == null) return Collections.emptyList();
            List<ResponseMapaDTO> listaMapa = Arrays.asList(resposta);

            listaMapa.forEach(item -> correcaoMonetariaService.aplicarCorrecaoMapa(item, dadosProfissionalDTO.getAnoReferencia()));

           return listaMapa;

    }

}
