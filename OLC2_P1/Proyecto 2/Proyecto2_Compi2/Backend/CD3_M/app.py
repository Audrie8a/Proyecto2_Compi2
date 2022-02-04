from flask import Flask, request, jsonify
from flask_cors import CORS
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
@app.route('/compilar', methods=['POST'])
def compile():
    data = main.execute(request.json['code'])
    return jsonify(data)


# Mirilla
@app.route('/mirilla', methods=['POST'])
def optimizar_mirilla():
    data = main.execute_mirilla(request.json['code'])
    return jsonify(data)


# Bloque
@app.route('/bloque', methods=['POST'])
def optimizar_bloque():
    data = main.execute_bloque(request.json['code'])
    return jsonify(data)


@app.route('/dev', methods=['GET'])
def dev_compile():
    data = main.dev_compilier()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)