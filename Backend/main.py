from typing import Text
from flask import *
from werkzeug.wrappers import response
from flask_cors import CORS, cross_origin

app= Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello world! Audrie'

@app.route('/Entrada', methods=['POST'])
def Entrada():
    Texto= request.json['Texto']
    Texto="Respuesta: "+Texto;
    print(Texto)
    response= jsonify( {"Respuesta": "Respuesta"+Texto})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)