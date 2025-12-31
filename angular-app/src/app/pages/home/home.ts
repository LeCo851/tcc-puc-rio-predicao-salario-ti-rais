import { ChangeDetectionStrategy, ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { SalarioService } from '../../salario.service';
import { DadosProfissional, PrevisaoSalario } from '../../models';
import { mapaCargos } from '../../data/cargos.const';
import {LISTA_SETORES} from '../../data/setores.const';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Home {

  // Variáveis de Controle
  carregando: boolean = false;
  erro: string = '';
  resultado: PrevisaoSalario | null = null;

  mapaCargos = mapaCargos;
  setoresOpcoes = LISTA_SETORES;

  // Variável para controlar a Senioridade (Faixa)
  // Se estiver vazia, usamos a idade manual.
  senioridadeSelecionada: string = '';

  // Objeto de Dados do Formulário (Valores Padrão)
  dados: DadosProfissional = {
    ano_referencia: 2024,
    cargo: 'Analista de desenvolvimento de sistemas',
    escolaridade: 'Superior Completo',
    idade: 30, // Valor padrão visual para o input manual
    raca: 'Branca',
    setor: 'Instituiçoes de crédito, seguros e capitalizaçao',
    sexo: 'Masculino',
    tamanho_empresa: 'De 100 a 249 funcionários',
    uf: 'SP',
    faixa_experiencia: undefined // Começa indefinido
  };

  // --- LISTAS PARA OS DROPDOWNS ---

  listaUfs: string[] = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
    'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
    'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
  ];

  listaOpcoesVisual: string[] = Object.keys(this.mapaCargos).sort((a, b) => a.localeCompare(b));

  listaAnos: number[] = [2019, 2020, 2021, 2022, 2023, 2024];

  // Nova lista para o Select de Experiência
  listaExperiencias = [
    { label: 'Júnior (Iniciante)', value: 'JUNIOR' },
    { label: 'Pleno (Intermediário)', value: 'PLENO' },
    { label: 'Sênior (Avançado)', value: 'SENIOR' },
    { label: 'Especialista / Master', value: 'ESPECIALISTA' }
  ];

  constructor(private service: SalarioService, private cdr: ChangeDetectorRef) {}

  // Função chamada pelo (ngSubmit)
  calcular() {
    this.erro = '';
    this.resultado = null;

    // 1. Validação Condicional
    // Só validamos a idade se o usuário NÃO selecionou uma faixa de experiência
    if (!this.senioridadeSelecionada) {
      if (!this.dados.idade || this.dados.idade < 16 || this.dados.idade > 80) {
        this.erro = 'Para idade manual, informe um valor entre 16 e 70 anos.';
        this.cdr.markForCheck();
        return;
      }
    }

    // 2. Prepara Tela
    this.carregando = true;
    this.cdr.markForCheck();

    const cargoOficial = this.mapaCargos[this.dados.cargo] || this.dados.cargo;

    // 3. Montagem Inteligente do Payload
    const dadosParaEnvio = {
      ...this.dados,
      cargo: cargoOficial,

      // Lógica Híbrida:
      // Se tem senioridade, manda ela e idade null.
      // Se não tem senioridade, manda idade e faixa null.
      faixa_experiencia: this.senioridadeSelecionada || undefined,
      idade: this.senioridadeSelecionada ? null : this.dados.idade
    };

    // 4. Chama Serviço
    this.service.preverSalario(dadosParaEnvio).subscribe({
      next: (res) => {
        console.log('>>> RESPOSTA DO JAVA:', res);
        console.log('>>> RESULTADO:', res.resultado);
        this.resultado = res;
        this.carregando = false;
        this.cdr.markForCheck();

        // Scroll suave para o resultado (opcional, melhora UX)
        setTimeout(() => {
          const el = document.getElementById('resultado-card');
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
      },
      error: (err: HttpErrorResponse) => {
        console.error('Erro na API:', err);
        if (err.status === 0) {
          this.erro = "Não foi possível conectar ao servidor.";
        } else {
          // Tenta pegar a mensagem amigável que vem do Java
          this.erro = err.error?.message || "Ocorreu um erro inesperado ao processar a previsão.";
        }
        this.carregando = false;
        this.cdr.markForCheck();
      }
    });
  }
}
