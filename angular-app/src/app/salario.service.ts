import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DadosProfissional, PrevisaoSalario } from './models';

@Injectable({
  providedIn: 'root'
})
export class SalarioService {

  // URL do seu Spring Boot (Backend)
  private readonly apiUrl = 'http://127.0.0.1:8080/api/salarios/prever';

  constructor(private readonly http: HttpClient) { }

  preverSalario(dados: DadosProfissional): Observable<PrevisaoSalario> {
    return this.http.post<PrevisaoSalario>(this.apiUrl, dados);
  }
}
