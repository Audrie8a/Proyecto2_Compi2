from flask import Flask,request, jsonify,render_template
from Analyzer.Panther import parser
from Environment.Listas import Listas
from flask_cors import CORS
from Reportes.Reportes import Reportes
from AnalyzerTree.PantherTree import Ast

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
auxiliar=""
@app.route("/Entrada", methods=['POST'])
def Entrada():
    Listas.LimpiarLsts()
    try:
        Texto= request.json['Texto']        
        auxiliar=Texto
        try:
            parser.parse(Texto)            
            Ast(Texto)
            mistakes=False
            if(len(Listas.getListError())!=0):
                mistakes=True
            response= jsonify( {"Respuesta": Listas.getListSaida(),
                        "Tamano": len(Listas.getListSaida()),
                        "Errores":str(mistakes)})
            Listas.printSaida()
            #response.headers.add("Access-Control-Allow-Origin", "*")
            
            return response
        except:
            print("Error al ejecutar instrucciones")
        return { 'msg': 'ERROR EJECUCION', 'code': 200 }
    except:
        return { 'msg': 'ERROR', 'code': 500 }

@app.route("/TablaErrores", methods=['GET'])
def Errores():
    if (len(Listas.getListError())!=0):
        response= jsonify({"Respuesta": Listas.getListError()})
        Listas.printErrores()
    else:
        response= jsonify({"Respuesta": "Error"})
    return  response


@app.route("/TablaSimbolos", methods=['GET'])
def Simbolos():
    if (len(Listas.getListaSimbolo())!=0):
        response= jsonify({"Respuesta": Listas.getListaSimbolo()})
    else:
        response= jsonify({"Respuesta": "Error"})
    return  response

@app.route("/getAst", methods=['GET'])
def getAst():
    
    if (len(Listas.getAst())!=0):
        response= jsonify({"Respuesta": Listas.getAst()})
    else:
        response= jsonify({"Respuesta": "Error"})
    return  response

@app.route("/")
def home():
    return "<h1>Hola me llamo audrie</h1>"