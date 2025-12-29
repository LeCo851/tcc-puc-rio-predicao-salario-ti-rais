import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HighchartsChartModule } from 'highcharts-angular';
import Highcharts from 'highcharts';

// Importação do módulo de mapa
import HC_map from 'highcharts/modules/map';

// Inicializa o módulo
HC_map(Highcharts);

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, HighchartsChartModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard implements OnInit {

  Highcharts: typeof Highcharts = Highcharts;
  chartOptions: Highcharts.Options | null = null;

  carregando: boolean = true;
  erro: string = '';

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.carregarMapa();
  }

  async carregarMapa() {
    try {
      this.carregando = true;
      this.erro = '';

      console.log('🔄 Carregando mapa (CDN)...');

      // 1. Busca o arquivo GeoJSON do CDN oficial do Highcharts para garantir o carregamento
      const response = await fetch('https://code.highcharts.com/mapdata/countries/br/br-all.geo.json');

      if (!response.ok) {
        throw new Error(`Erro ao baixar mapa do CDN (${response.status})`);
      }

      const mapGeoJSON = await response.json();
      console.log('✅ Mapa carregado! Tipo:', mapGeoJSON.type);

      // 2. Dados Fictícios
      const data = [
        ['br-sp', 8500], ['br-rj', 7200], ['br-mg', 6000], ['br-rs', 6500],
        ['br-pr', 6300], ['br-sc', 6800], ['br-ba', 4500], ['br-pe', 4800],
        ['br-df', 9000], ['br-am', 5000], ['br-ce', 4200], ['br-ac', 3500]
      ];

      // 3. Configuração
      this.chartOptions = {
        chart: {
          map: mapGeoJSON,
          height: 600,
          style: { fontFamily: 'Roboto, sans-serif' }
        },
        title: { text: 'Média Salarial por Estado' },
        credits: { enabled: false },
        mapNavigation: {
          enabled: true,
          buttonOptions: { verticalAlign: 'bottom' }
        },
        colorAxis: {
          min: 3000,
          max: 10000,
          minColor: '#E6F3FF',
          maxColor: '#003865',
          labels: { format: 'R$ {value}' }
        },
        plotOptions: {
          map: {
            allAreas: true,
            // CORREÇÃO AQUI: Forçamos o tipo para aceitar o número 0
            joinBy: ['hc-key', 0] as [string, any],
            dataLabels: {
              enabled: true,
              format: '{point.properties.hc-a2}'
            }
          }
        },
        series: [{
          type: 'map',
          name: 'Salário Médio',
          data: data
        }] as any
      };

      this.carregando = false;
      this.cdr.detectChanges(); // Força a atualização da tela

    } catch (e: any) {
      console.error('❌ ERRO:', e);
      this.erro = 'Erro ao desenhar mapa: ' + e.message;
      this.carregando = false;
      this.cdr.detectChanges(); // Força a atualização da tela em caso de erro
    }
  }
}
