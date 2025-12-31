import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HighchartsChartModule } from 'highcharts-angular';
import Highcharts from 'highcharts';
import HC_map from 'highcharts/modules/map';

// Inicializa o módulo de mapas
HC_map(Highcharts);

import { SalarioService } from '../../salario.service';
import { mapaCargos } from '../../data/cargos.const';
import {LISTA_SETORES} from '../../data/setores.const';


interface CustomPoint extends Highcharts.Point {
  salarioBase: string;
  salarioFinal: string;
  total: number;
  masc: number;
  fem: number;
  z: number;
  'hc-key': string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, HighchartsChartModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard implements OnInit {

  Highcharts: typeof Highcharts = Highcharts;
  chartOptions: Highcharts.Options | null = null;
  mapGeoJSON: any = null;

  carregando: boolean = true;
  erro: string = '';

  // Filtros
  listaCargos: string[] = Object.keys(mapaCargos).sort((a, b) => a.localeCompare(b));
  cargoSelecionado: string = 'Analista de desenvolvimento de sistemas';
  anosDisponiveis: number[] = [2019, 2020, 2021, 2022, 2023, 2024];
  anoSelecionado: number = 2024;
  setoresOpcoes = LISTA_SETORES;

  opcoesExperiencia = [
    { label: 'Júnior (Iniciante)', value: 'JUNIOR' },
    { label: 'Pleno (Intermediário)', value: 'PLENO' },
    { label: 'Sênior (Avançado)', value: 'SENIOR' },
    { label: 'Especialista / Master', value: 'ESPECIALISTA' }
  ];
  faixaSelecionada: string = 'PLENO';
  idadeManual: number = 32;

  setorSelecionado: string = 'Instituiçoes de crédito, seguros e capitalizaçao';
  tamanhoEmpresaSelecionado: string = 'De 50 a 99 funcionários';
  escolaridadeSelecionada: string = 'Superior Completo';

  constructor(private readonly salarioService: SalarioService, private readonly cdr: ChangeDetectorRef) {}

  async ngOnInit() {
    if (typeof Highcharts === 'object') {
      await this.carregarMapaBase();
    }
  }

  async carregarMapaBase() {
    try {
      this.carregando = true;
      const response = await fetch('https://code.highcharts.com/mapdata/countries/br/br-all.geo.json');
      if (!response.ok) throw new Error('Erro ao baixar geometria do mapa.');
      this.mapGeoJSON = await response.json();
      this.atualizarDadosMapa();
    } catch (e: any) {
      console.error(e);
      this.erro = 'Erro ao carregar mapa.';
      this.carregando = false;
      this.cdr.detectChanges();
    }
  }

  atualizarDadosMapa() {
    this.carregando = true;
    this.erro = '';

    const cargoOficial = mapaCargos[this.cargoSelecionado] || this.cargoSelecionado;
    const filtros = {
      cargo: cargoOficial,
      ano_referencia: Number(this.anoSelecionado),
      faixa_experiencia: this.faixaSelecionada || null,
      idade: this.faixaSelecionada ? null : this.idadeManual,
      escolaridade: this.escolaridadeSelecionada,
      tamanho_empresa: this.tamanhoEmpresaSelecionado,
      setor: this.setorSelecionado,
      sexo: 'Masculino',
      raca: 'Branca'
    };

    this.salarioService.obterDadosMapa(filtros).subscribe({
      next: (dadosBackend: any[]) => {
        if (!dadosBackend?.length) {
          this.erro = 'Sem dados para os filtros.';
        } else {
          this.renderizarGrafico(dadosBackend);
        }
        this.carregando = false;
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        this.erro = err.error?.message || 'Erro ao carregar dados.';
        this.carregando = false;
        this.cdr.detectChanges();
      }
    });
  }

  renderizarGrafico(dados: any[]) {
    const mapData = dados.map(item => ({
      'hc-key': item.uf,
      value: item.salario_estimado,
      salarioBase: item.salarioEstimadoFormatado,
      salarioFinal: item.salarioCorrigido,
      total: item.quantidade_total || 0,
      masc: item.quantidade_masculino || 0,
      fem: item.quantidade_feminino || 0
    }));

    const bubbleData = dados.map(item => ({
      'hc-key': item.uf,
      z: item.quantidade_total
    }));

    this.chartOptions = {
      chart: {
        map: this.mapGeoJSON,
        height: 650,
        style: { fontFamily: 'Segoe UI, sans-serif' },
        backgroundColor: 'transparent'
      },
      title: { text: '' },
      credits: { enabled: false },

      plotOptions: {
        series: {
          states: {
            inactive: {
              opacity: 1
            }
          }
        }
      },

      mapNavigation: {
        enabled: true,
        buttonOptions: { verticalAlign: 'bottom' },
        enableMouseWheelZoom: false
      },

      legend: {
        enabled: true,

        // Posicionamento
        align: 'right',
        verticalAlign: 'bottom',
        layout: 'vertical',
        floating: true, // Flutua sobre o mapa
        x: -20,         // Afasta 20px da borda direita
        y: -60,         // Sobe 60px para não bater na borda inferior
        // Estilo do "Cartão"
        backgroundColor: 'rgba(255, 255, 255, 0.95)', // Quase branco sólido
        borderRadius: 8,
        borderWidth: 1,
        borderColor: '#e0e0e0',
        shadow: {
          color: 'rgba(0,0,0,0.1)',
          offsetX: 1,
          offsetY: 1,
          width: 3
        },
        padding: 16, // Mais respiro interno

        // Espaçamento entre os itens (Salário e Volume)
        itemMarginBottom: 10,
        itemMarginTop:10,

        // Estilo do Texto
        itemStyle: {
          color: '#444',
          fontSize: '11px',
          fontWeight: '600',
          fontFamily: 'Segoe UI, sans-serif'
        },

        // Título (Opcional)
        title: {
          text: 'Legenda:',
          style: {
            fontSize: '10px',
            color: '#888',
            textTransform: 'uppercase',
            fontWeight: 'bold'
          }
        },

        // Desativa a legenda complexa de bolhas que estava atrapalhando
        bubbleLegend: {
          enabled: false
        }
      },


      colorAxis: {
        reversed:false,
        minColor: '#E1F5FE',
        maxColor: '#01579B',
        labels: {
          format: 'R$ {value:,.0f}',
          style: { fontSize: '11px', fontWeight: 'bold', color: '#555' }
        }
      },

      tooltip: {
        useHTML: true,
        backgroundColor: 'rgba(255, 255, 255, 0.98)',
        borderRadius: 12,
        shadow: true,
        headerFormat: '',
        pointFormatter: function(this: any) {
          const chart = this.series.chart;
          const mapPoint = chart.series[0].data.find((d: any) => d['hc-key'] === this['hc-key']) as CustomPoint;
          const p = mapPoint || this;

          return `
            <div style="font-family: 'Segoe UI', sans-serif; min-width: 210px; color: #333; padding: 10px;">
              <div style="font-weight: 700; font-size: 14px; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 8px;">
                ${this.name || p.name}
              </div>
              <div style="background: #f0f7ff; border-radius: 6px; padding: 8px; text-align: center; margin-bottom: 8px; border: 1px solid #d0e3ff;">
                <div style="font-size: 10px; color: #5c7cfa; text-transform: uppercase; font-weight: 700;">Média Salarial</div>
                <div style="font-size: 18px; color: #0044cc; font-weight: 800;">${p.salarioFinal}</div>
              </div>
              <div style="font-size: 11px; color: #555;">
                <div>👥 <b>Amostra:</b> ${p.total} profissionais</div>
                <div>👨 <b>Homens:</b> ${p.masc} | 👩 <b>Mulheres:</b> ${p.fem}</div>
              </div>
            </div>
          `;
        }
      },

      series: [
        {
          type: 'map',
          name: 'Salário Estimado',
          data: mapData,
          colorAxis: 0,
          joinBy: ['hc-key', 'hc-key'],
          allAreas: true,
          states: {
            hover: {
              brightness: 0
            },
            legendIndex:2
          },
          dataLabels: {
            enabled: true,
            format: '{point.properties.hc-a2}',
            style: { fontSize: '10px', fontWeight: 'bold', textOutline: 'none', pointerEvents: 'none' }
          }
        },
        {
          type: 'mapbubble',
          name: 'Volume (Qtd Pessoas)',
          data: bubbleData,
          joinBy: ['hc-key', 'hc-key'],
          colorAxis: false,
          minSize: 6,
          maxSize: '20%',
          color: 'rgba(255, 140, 0, 0.6)',
          borderColor: 'white',
          borderWidth: 1,
          states: {
            hover: {
              color: 'rgba(255, 140, 0, 0.9)',
              brightness: 0
            }
            ,legendIndex: 1
          },
          tooltip: { pointFormat: '' }
        }
      ] as any
    };
  }

  protected readonly LISTA_SETORES = LISTA_SETORES;
}
