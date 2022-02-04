from flask import Flask, request, jsonify
from flask_cors import CORS
from src.interprete.compilador.simbolos.Listas import Listas
import src.controller.main as main

app = Flask(__name__)
CORS(app)

# ==============================================================================
# RUTAS
# ==============================================================================
# Prinicipal
@app.route('/')
def index():
    return jsonify(main.get_proyect_data())


# Compilar
@app.route('/Entrada', methods=['POST'])
def Entrada():
    try:
        data = main.execute(request.json['Texto'])
        return jsonify(data)
    except:
        print("Error al ejecutar instrucciones")
        return { 'msg': 'ERROR EJECUCION', 'code': 200 }


# Mirilla
@app.route('/Mirilla', methods=['POST'])
def optimizar_mirilla():
    data = main.execute_mirilla(request.json['Texto'])
    return jsonify(data)


# Bloque
@app.route('/Bloques', methods=['POST'])
def optimizar_bloque():
    data = main.execute_bloque(request.json['Texto'])
    return jsonify(data)


@app.route('/dev', methods=['GET'])
def dev_compile():
    data = main.dev_compilier()
    return jsonify(data)


@app.route("/TablaErrores", methods=['GET'])
def Errores():
    if (len(Listas.lstError)!=0):
        response= jsonify({"Respuesta": Listas.lstError})

    else:
        response= jsonify({"Respuesta": "Error"})
    return  response

@app.route("/TablaSimbolos", methods=['GET'])
def Simbolos():
    if (len(Listas.lstSimbolos)!=0):
        response= jsonify({"Respuesta": Listas.lstSimbolos})

    else:
        response= jsonify({"Respuesta": "Error"})
    return  response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)