import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ReportesService } from 'src/app/Servicios/reportes.service';


@Component({
  selector: 'app-reportes',
  templateUrl: './reportes.component.html',
  styleUrls: ['./reportes.component.css']
})
export class ReportesComponent implements OnInit {

  imageErrores?:string;
  Errores:any;
  Simbolos:any;
  Optimizacion:any;
  AST: any;
  txtSalida:string="";

  constructor(public reporteService:ReportesService ,
    public _activatedRoute: ActivatedRoute,
    public _router: Router) { } 

  ngOnInit(): void {
    this.AsignarReporte();
  }

  AsignarReporte(){
    this.imageErrores='../../../assets/RepMistakes.png'
  }

  step = 0;

  setStep(index: number) {
    this.step = index;
  }

  nextStep() {
    this.step++;
  }

  prevStep() {
    this.step--;
  }


  downloadFile(Rep: Number){
    let link = document.createElement("a");
    link.download = "filename";
    if (Rep==1){
      window.open("https://olc2-audrie8a.herokuapp.com/TablaErrores", "_blank");

    }else if (Rep==2){
      link.href = "../../../assets/RepSimbolos.png";
    }else{
      link.href = "../../../assets/Ast.png";
    }
    
    
    link.click();
  }

  async cragarTablaErrores(){
    this.Errores=[]
    let aux= await this.reporteService.getLstErrores();
    let json=JSON.stringify(aux)
      let obj= JSON.parse(json) 
    if(obj.Respuesta!='Error'){
      
      this.Errores=obj.Respuesta;
    }else{
      alert("No hay errores semánticos que mostrar!");
    }
  }

  async cargarTablaOptimizacion(){
    this.Errores=[]
    let aux= await this.reporteService.getLstOptimizado();
    let json=JSON.stringify(aux)
      let obj= JSON.parse(json) 
    if(obj.Respuesta!='Error'){
      
      this.Optimizacion=obj.Respuesta;
    }else{
      alert("No hay reglas de optimización que mostrar!");
    }
  }


  async cragarTablaSimbolos(){
    this.Simbolos=[]
    let aux= await this.reporteService.getLstSimbolos();
    let json=JSON.stringify(aux)
      let obj= JSON.parse(json) 
    if(obj.Respuesta!='Error'){
      
      this.Simbolos=obj.Respuesta;
    }else{
      alert("No hay símbolos que mostrar!");
    }
  }

  d3(){
    let aux="";
    this.AST.forEach((element: string) => {
      aux+=element+"\n";
    });

      this.txtSalida=aux;
      alert(aux)
    //graphviz("#graph")    
    //.renderDot(aux)
  }
  limpiar(opcion: Number){
    if(opcion==1){
      this.Errores=[]
    }else if(opcion==3){
      this.Simbolos=[] 
    }else if(opcion==2){
      this.Optimizacion=[]
    }
    
   
    
  }
}
