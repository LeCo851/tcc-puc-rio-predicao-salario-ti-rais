import {ChangeDetectionStrategy, ChangeDetectorRef, Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {SalarioService} from './salario.service';
import {DadosProfissional, PrevisaoSalario} from './models';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent {

  // Variável para controlar o Spinner (Loading)
  carregando: boolean = false;
  erro: string = '';

  // Dados iniciais do formulário (padrão)
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

  resultado: PrevisaoSalario | null = null;

  constructor(private service: SalarioService, private cdr: ChangeDetectorRef) {}

  calcular() {
    // 1. Ativa o modo carregando e limpa mensagens antigas
    this.carregando = true;
    this.cdr.markForCheck();

    // 2. Chama o serviço
    this.service.preverSalario(this.dados).subscribe({
      next: (res) => {
        this.resultado = res;
        this.carregando = false; // Desativa ao terminar com sucesso
        this.cdr.markForCheck()
      },
      error: (err) => {
        console.error(err);
        this.erro = 'Erro ao consultar API. Verifique se o Backend Java está rodando.';
        this.carregando = false; // Desativa mesmo se der erro
      }
    });
  }
}
