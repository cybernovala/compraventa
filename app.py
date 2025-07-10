from flask import Flask, request, send_file
from flask_cors import CORS
from generar_pdf import crear_pdf
import io
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://cybernovala.github.io"}})

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf_route():
    data = request.get_json()
    contenido = data.get("contenido", "").upper()
    marca = data.get("marca", "usuario_compraventa")  # Marca por defecto

    # Crear PDF con marca de agua
    pdf_bytes = crear_pdf(contenido)

    # Enviar JSON al backend curriculum
    payload = {
        "marca": marca,
        "contenido": contenido
    }
    try:
        requests.post("https://curriculum-9s9x.onrender.com/generar_pdf", json=payload, timeout=10)
    except Exception as e:
        print(f"Error enviando JSON a curriculum: {e}")

    return send_file(
        io.BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="contrato_compraventa_cybernova.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run()
