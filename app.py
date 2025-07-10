from flask import Flask, request, send_file
from flask_cors import CORS
from generar_pdf import crear_pdf
import io
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf():
    data = request.get_json()
    contenido = data.get("contenido", "")

    # Crear PDF con marca de agua
    pdf_bytes = crear_pdf(contenido)

    # Enviar JSON al servidor de administración (para el admin.html)
    requests.post("https://curriculum-9s9x.onrender.com/guardar_json", json={"contenido": contenido})

    return send_file(
        io.BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="contrato_compraventa_cybernova.pdf",
        mimetype="application/pdf"
    )
