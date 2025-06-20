from flask import Flask, request, send_file
from flask_cors import CORS
from generar_pdf import crear_pdf
import io

app = Flask(__name__)
CORS(app)

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf():
    data = request.get_json()
    contenido = data.get("contenido", "").upper()
    pdf_bytes = crear_pdf(contenido)
    return send_file(
        io.BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="contrato_compraventa.pdf",
        mimetype="application/pdf"
    )
