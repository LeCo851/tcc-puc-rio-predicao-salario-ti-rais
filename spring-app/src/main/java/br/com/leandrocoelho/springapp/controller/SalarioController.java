package br.com.leandrocoelho.springapp.controller;

import br.com.leandrocoelho.springapp.dto.DadosProfissionalDTO;
import br.com.leandrocoelho.springapp.dto.ResponseMapaDTO;
import br.com.leandrocoelho.springapp.dto.ResponsePrevisaoSalarioDTO;
import br.com.leandrocoelho.springapp.service.MapaService;
import br.com.leandrocoelho.springapp.service.SalarioService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/salarios")
@CrossOrigin(origins = "http://localhost:4200")
@RequiredArgsConstructor

public class SalarioController {

    private final SalarioService salarioService;
    private final MapaService mapaService;

    @PostMapping("/prever")
    public ResponseEntity<ResponsePrevisaoSalarioDTO> prever(@RequestBody DadosProfissionalDTO dadosProfissionalDTO){

            ResponsePrevisaoSalarioDTO resultado = salarioService.obterEstimativa(dadosProfissionalDTO);
            return ResponseEntity.ok(resultado);

    }


    @PostMapping("/mapa")
    public ResponseEntity<List<ResponseMapaDTO>> buscarDadosMapa(@RequestBody DadosProfissionalDTO dadosProfissionalDTO){

            List<ResponseMapaDTO> resultado = mapaService.obterDadosMapa(dadosProfissionalDTO);
            return ResponseEntity.ok(resultado);

    }

}
