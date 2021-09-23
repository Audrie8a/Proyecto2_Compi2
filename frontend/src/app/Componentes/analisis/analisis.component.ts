import { Component, OnInit,Renderer2,ElementRef  } from '@angular/core';
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
    public _router: Router,
    private renderer: Renderer2,
    private element: ElementRef) { }

  txtEntrada:string ="";
  lstSalida:any=[] 
  txtSalida:string="...";   

  ngOnInit(): void {
  }

  async Analizar(){
    let respuesta = await this.analisisService.sendEntrada(this.txtEntrada);
    if(respuesta!= null){
      alert("Analizando");
      const json = JSON.stringify(respuesta);
      const obj = JSON.parse(json);
      if(obj.Errores=='True'){
        alert("Se conetraron errores!");
      }
      this.lstSalida=obj.Respuesta;
      this.txtSalida="";
      for(let x=0; x< obj.Tamano;x++) {
        if (this.lstSalida[x][1]==="print"){
          this.txtSalida+=this.lstSalida[x][0];
        }else{
          this.txtSalida+="\n"+this.lstSalida[x][0]
        }
      }
      
      
    }else{
      alert("Error: No se logró comunicación");
    }
    
  }

  limpiar(){
    this.txtEntrada="";
    this.txtSalida="";
  }
}
