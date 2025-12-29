import { ChangeDetectionStrategy, ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { SalarioService } from '../../salario.service';
import { DadosProfissional, PrevisaoSalario } from '../../models';

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

  // Objeto de Dados do Formulário
  dados: DadosProfissional = {
    ano_referencia: 2024,
    cargo: 'Analista de desenvolvimento de sistemas',
    escolaridade: 'Superior Completo',
    idade: 30,
    raca: 'Branca',
    setor: 'Instituições Financeiras (Bancos)',
    sexo: 'Masculino',
    tamanho_empresa: 'De 50 a 99 funcionários',
    uf: 'SP'
  };

  // --- LISTAS PARA OS DROPDOWNS (Essenciais para o HTML não dar erro) ---

  listaUfs: string[] = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
    'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
    'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
  ];

  listaAnos: number[] = [2019, 2020, 2021, 2022, 2023, 2024];

  listaCargos: string[] = [
    "Administrador de banco de dados",
    "Administrador de redes",
    "Administrador de sistemas operacionais",
    "Administrador em segurança da informação",
    "Analista de desenvolvimento de sistemas",
    "Analista de pesquisa de mercado",
    "Analista de redes e de comunicação de dados",
    "Analista de sistemas de automação",
    "Analista de suporte computacional",
    "Analista de testes de tecnologia da informação",
    "Arquiteto de soluções de tecnologia da informação",
    "Cientista de dados",
    "Desenhista industrial gráfico (designer gráfico)",
    "Desenvolvedor de sistemas de tecnologia da informação (técnico)",
    "Diretor de tecnologia da informação",
    "Engenheiro de aplicativos em computação",
    "Engenheiro de equipamentos em computação",
    "Engenheiros de sistemas operacionais em computação",
    "Especialista em pesquisa operacional",
    "Estatístico",
    "Estatístico (estatística aplicada)",
    "Estatístico teórico",
    "Gerente de infraestrutura de tecnologia da informação",
    "Gerente de operação de tecnologia da informação",
    "Gerente de projetos de tecnologia da informação",
    "Gerente de segurança da informação",
    "Gerente de suporte técnico de tecnologia da informação",
    "Pesquisador em ciências da computação e informática",
    "Professor de computação (no ensino superior)",
    "Tecnólogo em gestão da tecnologia da informação",
    "Técnico de suporte ao usuário de tecnologia da informação"
  ];

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

    // 3. Chama Serviço
    this.service.preverSalario(this.dados).subscribe({
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
