import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-analisis',
  templateUrl: './analisis.component.html',
  styleUrls: ['./analisis.component.css']
})
export class AnalisisComponent implements OnInit {

  constructor() { }

  txtEntrada:string ="";
  ngOnInit(): void {
  }

  async Analizar(){
    alert(this.txtEntrada);
  }
}
