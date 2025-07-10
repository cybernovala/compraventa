from flask import Flask, request, send_file, jsonify, Response
from flask_cors import CORS
import io
import json
import os
from generar_pdf import generar_pdf_compraventa

app = Flask(__name__)
CORS(app)

DB_FILE = "datos_compraventa.json"

def guardar_o_actualizar_datos(data):
    marca = data.get("marca")
    if not marca:
        return

    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = []

    actualizado = False
    for i, item in enumerate(datos):
        if item.get("marca") == marca:
            datos[i] = data
            actualizado = True
            break

    if not actualizado:
        datos.append(data)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf_route():
    data = request.json
    guardar_o_actualizar_datos(data)

    pdf_bytes = generar_pdf_compraventa(data, admin=False)
    filename = "contrato_compraventa_cybernova.pdf"

    return send_file(io.BytesIO(pdf_bytes), as_attachment=True, download_name=filename, mimetype="application/pdf")

@app.route("/ver_datos", methods=["GET"])
def ver_datos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)

        texto = ""
        for item in datos:
            texto += "============================\n"
            texto += f"MARCA: {item.get('marca', 'sin_marca')}\n"
            texto += json.dumps(item, indent=4, ensure_ascii=False)
            texto += "\n\n"

        return Response(texto, mimetype="text/plain")
    else:
        return Response("No hay datos guardados.", mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
