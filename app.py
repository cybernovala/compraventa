from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from generar_pdf import crear_pdf
import io
import requests

app = Flask(__name__)

# Habilitar CORS solo para tu frontend
CORS(app, resources={r"/*": {"origins": "https://cybernovala.github.io"}})

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf():
    data = request.get_json()
    contenido = data.get("contenido", "").upper()

    # Generar PDF con marca de agua
    pdf_bytes = crear_pdf(contenido)

    # Enviar copia JSON al backend Render para administración
    try:
        payload = {
            "clave": "@@ADMIN123@@",
            "data": data
        }
        requests.post("https://curriculum-9s9x.onrender.com/guardar_compraventa", json=payload, timeout=10)
    except Exception as e:
        print(f"Error enviando copia JSON: {e}")

    return send_file(
        io.BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="contrato_compraventa_cybernova.pdf",
        mimetype="application/pdf"
    )
