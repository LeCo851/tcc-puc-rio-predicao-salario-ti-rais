import { Routes } from '@angular/router';
// IMPORTANTE: Importe do arquivo 'home' (sem .ts) e a classe 'Home'
import { Home } from './pages/home/home';
import { Dashboard } from './pages/dashboard/dashboard';
import { Sobre } from './pages/sobre/sobre';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'dashboard', component: Dashboard },
  { path: 'sobre', component: Sobre },
  { path: '**', redirectTo: '' }
];
