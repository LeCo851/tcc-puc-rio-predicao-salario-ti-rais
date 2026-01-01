import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DadosProfissional, PrevisaoSalario } from './models';
import {environment} from '../environments/environment';

export interface ResultadoMapa {
  uf: string;
  salario_estimado: number;
  salarioCorrigido: string;
  salarioEstimadoFormatado: string;
  fatorCorrecao: number;
  quantidade_total: number;
  quantidade_masculino: number;
  quantidade_feminino: number;
}

@Injectable({
  providedIn: 'root'
})
export class SalarioService {

  // URL do seu Spring Boot (Backend)
  private readonly apiUrl = `${environment.apiBaseUrl}/api/salarios/prever`;
  private readonly mapaUrl = `${environment.apiBaseUrl}/api/salarios/mapa`;

  constructor(private readonly http: HttpClient) { }

  preverSalario(dados: DadosProfissional): Observable<PrevisaoSalario> {
    return this.http.post<PrevisaoSalario>(this.apiUrl, dados);
  }
  obterDadosMapa(filtros: any): Observable<ResultadoMapa[]> {
    return this.http.post<ResultadoMapa[]>(this.mapaUrl, filtros);
  }
}
