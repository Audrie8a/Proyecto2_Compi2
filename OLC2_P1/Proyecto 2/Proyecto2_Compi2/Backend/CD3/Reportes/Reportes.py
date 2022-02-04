from typing import List
from graphviz import Source
from Environment.Listas import Listas
import graphviz
import os
import shutil

class Reportes:
    lstError=[]
    lstSalida=[]

    @staticmethod
    def Graficar(Contenido: str,Nombre: str):
        
        Dot_Content="digraph G {"
        Dot_Content+="nodo[shape=plaintext label=<"
        Dot_Content+=Contenido
        Dot_Content+=">];}"

        os.environ["PATH"] += os.pathsep + r'D:\Segundo Semestre 2021\Compi 2\Lab\Proyecto 1\Backend\Panther\Reportes'
        file = open("./"+Nombre+".dot", "w")
        file.write(Dot_Content)
        file.close()

        os.system('dot -Tpng RepMistakes.dot -o ./static/RepMistakes.jpg')
        
        Listas.LimpiarLsts()
        #shutil.move("D:\Segundo Semestre 2021\Compi 2\Lab\Proyecto 1\/"+Nombre+".png", "D:\Segundo Semestre 2021\Compi 2\Lab\Proyecto 1\/frontend\src\/assets\/"+Nombre+".png")

        
        

    def Tabla_Errores():
        Contenido=""
        Contenido+="<table >\n"
        Contenido+="<tr>\n"
        Contenido+="<td >No</td>\n"
        Contenido+="<td >Descripcion</td>\n"
        Contenido+="<td >Linea</td>\n"
        Contenido+="<td >Columna</td>\n"
        Contenido+="<td >Fecha y Hora</td>\n"
        Contenido+="</tr>\n"
        if len(Listas.getListError())!=0:
            for var in Listas.getListError():
                Contenido+="<tr>\n"
                Contenido+="<td >"+str(var[0])+"</td>\n"
                Contenido+="<td >"+str(var[1])+"</td>\n"
                Contenido+="<td >"+str(var[2])+"</td>\n"
                Contenido+="<td >"+str(var[3])+"</td>\n"
                Contenido+="<td >"+str(var[4])+"</td>\n"
                Contenido+="</tr>\n"
                
        else:
            Contenido+="<tr>\n"
            Contenido+="<td  colspan=\"5\">No se encontraron Errores semanticos!</td>\n"
            Contenido+="</tr>\n"

        Contenido+="</table>\n"
        Reportes.Graficar(Contenido,"RepMistakes")


    

    