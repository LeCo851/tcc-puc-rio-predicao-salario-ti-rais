package br.com.leandrocoelho.springapp.controller;

import br.com.leandrocoelho.springapp.dto.DadosProfissionalDTO;
import br.com.leandrocoelho.springapp.dto.PrevisaoSalarioDTO;
import br.com.leandrocoelho.springapp.service.SalarioService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/salarios")
@CrossOrigin(origins = "http://localhost:4200")
@RequiredArgsConstructor
public class SalarioController {

    private final SalarioService salarioService;

    @PostMapping("/prever")
    public ResponseEntity<PrevisaoSalarioDTO> prever(@RequestBody DadosProfissionalDTO dadosProfissionalDTO){
        PrevisaoSalarioDTO resultado = salarioService.obterEstimativa(dadosProfissionalDTO);
        return ResponseEntity.ok(resultado);
    }

}
