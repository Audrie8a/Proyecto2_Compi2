import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class ReportesService {

  constructor(private httpClient: HttpClient) { }

  //"https://olc2-audrie8a.herokuapp.com/"   "http://10.154.136.37:8000/"//
  url:string="http://10.154.136.37:8000/"
  
  getLstErrores(){
    const ruta= this.url+"TablaErrores";
    return this.httpClient.get(ruta).toPromise();
  }

  getLstSimbolos(){
    const ruta= this.url+"TablaSimbolos";
    return this.httpClient.get(ruta).toPromise();
  }



  getLstOptimizado(){
    const ruta= this.url+"TablaOptimizado";
    return this.httpClient.get(ruta).toPromise();
  }
}
