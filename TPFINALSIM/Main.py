# archivo: Main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from Simulador import Simulador

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def bienvenida():
    return jsonify({ 'mensaje' : 'Simulador de mecanógrafa funcionando'})

@app.route('/simular', methods=['POST'])
def simular():
    datos = request.get_json()

    try:
        media_llegada = float(datos.get('media_llegada'))
        tiempo_reparacion = float(datos.get('tiempo_reparacion'))
        trabajos_a_completar = int(datos.get('trabajos_a_completar'))
        iteraciones = int(datos.get('iteraciones'))

        if media_llegada <= 0 or tiempo_reparacion < 0 or trabajos_a_completar <= 0 or iteraciones <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Datos de entrada inválidos. Asegúrese de ingresar números positivos."}), 400

    simulador = Simulador(media_llegada, tiempo_reparacion, trabajos_a_completar)
    resultados = simulador.ejecutar(iteraciones)

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
