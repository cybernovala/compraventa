from flask import Flask, request, send_file
from flask_cors import CORS
from generar_pdf import crear_pdf
import io
import requests
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Para que admin funcione desde cualquier origen

DB_FILE = "datos_guardados.json"

def enviar_datos_al_curriculum(data_json):
    url_curriculum = "https://curriculum-9s9x.onrender.com/generar_pdf"
    try:
        resp = requests.post(url_curriculum, json=data_json, timeout=10)
        print("✅ Datos enviados al JSON curriculum:", resp.status_code)
        return resp.status_code
    except Exception as e:
        print(f"⚠️ Error enviando datos al curriculum: {e}")
        return None

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf_route():
    data = request.get_json()
    contenido = data.get("contenido", "").upper()
    marca = f"usuario_{int(time.time() * 1000)}"
    data_json = {
        "marca": marca,
        "contenido": contenido
    }
    enviar_datos_al_curriculum(data_json)

    pdf_bytes = crear_pdf(contenido, admin=False)
    return send_file(io.BytesIO(pdf_bytes), as_attachment=True, download_name="contrato_compraventa_cybernova.pdf", mimetype="application/pdf")

@app.route("/generar_pdf_admin", methods=["POST"])
def generar_pdf_admin_route():
    datos = request.json
    clave = datos.get("clave")
    if clave != "@@ADMIN123@@":
        return {"error": "Clave incorrecta"}, 403

    contenido = datos.get("data", {}).get("contenido", "")
    if not contenido:
        return {"error": "No se encontró contenido"}, 400

    # Generar PDF sin marca de agua
    pdf_bytes = crear_pdf(contenido, admin=True)
    return send_file(io.BytesIO(pdf_bytes), as_attachment=True, download_name="contrato_compraventa_sin_marca.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
