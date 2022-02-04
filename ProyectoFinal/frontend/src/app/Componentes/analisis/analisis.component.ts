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
    opt=""
    txtEntrada:string ="";
    lstSalida:any=[] 
    txtSalida:string="...";   

  ngOnInit(): void {
  }

  async Analizar(){
    if (this.opt=="1"){
      alert("Compilar");
      
      let respuesta = await this.analisisService.sendEntrada(this.txtEntrada);
      if(respuesta!= null){
        alert("Analizando");
        const json = JSON.stringify(respuesta);
        const obj = JSON.parse(json);
        if(obj.Errores=='True'){
          alert("Se conetraron errores!");
        }
        this.txtSalida=obj.Respuesta;       
        
      }else{
        alert("Error: No se logró comunicación");
      }


    }else if (this.opt=="2"){
      alert("Mirilla");
      let respuesta = await this.analisisService.sendMirilla(this.txtEntrada);
      if(respuesta!= null){
        alert("Analizando");
        const json = JSON.stringify(respuesta);
        const obj = JSON.parse(json);
        if(obj.Errores=='True'){
          alert("Se conetraron errores!");
        }
        this.txtSalida=obj.Respuesta;       
        
      }else{
        alert("Error: No se logró comunicación");
      }
    }else if (this.opt=="3"){
      alert("Bloques")
      let respuesta = await this.analisisService.sendBloques(this.txtEntrada);
      if(respuesta!= null){
        alert("Analizando");
        const json = JSON.stringify(respuesta);
        const obj = JSON.parse(json);
        if(obj.Errores=='True'){
          alert("Se conetraron errores!");
        }
        this.txtSalida=obj.Respuesta;       
        
      }else{
        alert("Error: No se logró comunicación");
      }
    }else{
      alert("Por favor elija una opción!");
    }


    
    
    
  }

  limpiar(){
    this.txtEntrada="";
    this.txtSalida="";
  }
}
