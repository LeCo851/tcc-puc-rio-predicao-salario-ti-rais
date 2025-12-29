import { ChangeDetectionStrategy, ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { SalarioService } from '../../salario.service';
import { DadosProfissional, PrevisaoSalario } from '../../models';
import {mapaCargos} from '../../data/cargos.const';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule], // Importando módulos essenciais
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
  // Objeto de Dados do Formulário
  dados: DadosProfissional = {
    ano_referencia: 2024,
    cargo: 'Analista de desenvolvimento de sistemas',
    escolaridade: 'Superior Completo',
    idade: 30,
    raca: 'Branca',
    setor: 'Instituições Financeiras (Bancos)',
    sexo: 'Masculino',
    tamanho_empresa: 'De 100 a 249 funcionários',
    uf: 'SP'
  };

  // --- LISTAS PARA OS DROPDOWNS (Essenciais para o HTML não dar erro) ---

  listaUfs: string[] = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
    'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
    'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
  ];

  listaOpcoesVisual : string[] = Object.keys(this.mapaCargos).sort((a, b) => a.localeCompare(b));

  listaAnos: number[] = [2019, 2020, 2021, 2022, 2023, 2024];

  constructor(private service: SalarioService, private cdr: ChangeDetectorRef) {}

  // Função chamada pelo (ngSubmit)
  calcular() {
    // 1. Validação
    if (this.dados.idade < 16 || this.dados.idade > 70) {
      this.erro = 'A idade deve estar entre 16 e 70 anos.';
      this.cdr.markForCheck();
      return;
    }

    // 2. Prepara Tela
    this.carregando = true;
    this.erro = '';
    this.resultado = null;
    this.cdr.markForCheck();

    const cargoOficial = this.mapaCargos[this.dados.cargo] || this.dados.cargo;

    const dadosParaEnvio = {
      ...this.dados,
      cargo: cargoOficial
    };
    // 3. Chama Serviço
    this.service.preverSalario(dadosParaEnvio).subscribe({
      next: (res) => {
        this.resultado = res;
        this.carregando = false;
        this.cdr.markForCheck();
      },
      error: (err: HttpErrorResponse) => {
        if(err.status === 0){
          this.erro = "Não foi possível conectar ao servidor.";
        } else {
          this.erro = err.error?.message || "Ocorreu um erro inesperado.";
        }
        this.carregando = false;
        this.cdr.markForCheck();
      }
    });
  }
}
