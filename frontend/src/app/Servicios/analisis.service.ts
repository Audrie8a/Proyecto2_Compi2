import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class AnalisisService {

  constructor(private httpClient: HttpClient) { }
  url:string="http://10.154.136.37:8000/"
  sendEntrada(Texto: string){
    const ruta= this.url+"Entrada";
    const data = {Texto};    
    return this.httpClient.post(ruta,data).toPromise();
  }
}
