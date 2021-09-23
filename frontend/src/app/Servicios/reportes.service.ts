import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class ReportesService {

  constructor(private httpClient: HttpClient) { }

  //"https://olc2-audrie8a.herokuapp.com/"   "http://10.154.136.37:8000/"//
  url:string="https://olc2-audrie8a.herokuapp.com/"
  
  getLstErrores(){
    const ruta= this.url+"TablaErrores";
    return this.httpClient.get(ruta).toPromise();
  }

  getLstSimbolos(){
    const ruta= this.url+"TablaSimbolos";
    return this.httpClient.get(ruta).toPromise();
  }

  getAst(){
    const ruta= this.url+"getAst";
    return this.httpClient.get(ruta).toPromise();
  }
}
