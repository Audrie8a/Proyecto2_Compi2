import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AnalisisService } from 'src/app/Servicios/analisis.service';

@Component({
  selector: 'app-analisis',
  templateUrl: './analisis.component.html',
  styleUrls: ['./analisis.component.css']
})
export class AnalisisComponent implements OnInit {

  constructor( public analisisService: AnalisisService,
    public _activatedRoute: ActivatedRoute,
    public _router: Router) { }

  txtEntrada:string ="";
  ngOnInit(): void {
  }

  async Analizar(){
    let respuesta = await this.analisisService.sendEntrada(this.txtEntrada);
    if(respuesta!= null){
      alert("Analizando");
    }else{
      alert("Error: No se logró comunicación")
    }
    
  }
}
