import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { InicioComponent } from './Componentes/inicio/inicio.component';
import { AnalisisComponent } from './Componentes/analisis/analisis.component';
import { ReportesComponent } from './Componentes/reportes/reportes.component';
import {MatTabsModule} from '@angular/material/tabs';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DatosComponent } from './Componentes/datos/datos.component';

@NgModule({
  declarations: [
    AppComponent,
    InicioComponent,
    AnalisisComponent,
    ReportesComponent,
    DatosComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,

    MatTabsModule,

    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
