import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DadosProfissional, PrevisaoSalario } from './models';

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
  private readonly apiUrl = 'http://127.0.0.1:8080/api/salarios/prever';
  private readonly mapaUrl = 'http://localhost:8080/api/salarios/mapa';

  constructor(private readonly http: HttpClient) { }

  preverSalario(dados: DadosProfissional): Observable<PrevisaoSalario> {
    return this.http.post<PrevisaoSalario>(this.apiUrl, dados);
  }
  obterDadosMapa(filtros: any): Observable<ResultadoMapa[]> {
    return this.http.post<ResultadoMapa[]>(this.mapaUrl, filtros);
  }
}
