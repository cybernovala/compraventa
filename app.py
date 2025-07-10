from flask import Flask, request, send_file, jsonify, Response
from flask_cors import CORS, cross_origin
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
@cross_origin()
def generar_pdf_route():
    data = request.json
    guardar_o_actualizar_datos(data)

    pdf_bytes = generar_pdf_compraventa(data, admin=False)
    filename = "contrato_compraventa_cybernova.pdf"

    return send_file(io.BytesIO(pdf_bytes), as_attachment=True, download_name=filename, mimetype="application/pdf")

@app.route("/generar_pdf_admin", methods=["POST"])
@cross_origin()
def generar_pdf_admin_route():
    datos = request.json
    clave = datos.get("clave")
    if clave != "@@ADMIN123@@":
        return jsonify({"error": "Clave incorrecta"}), 403

    data_cv = datos.get("data")
    if not data_cv:
        return jsonify({"error": "Faltan datos"}), 400

    pdf_bytes = generar_pdf_compraventa(data_cv, admin=True)
    filename = "contrato_compraventa_sin_marca.pdf"

    return send_file(io.BytesIO(pdf_bytes), as_attachment=True, download_name=filename, mimetype="application/pdf")

@app.route("/ver_datos", methods=["GET"])
@cross_origin()
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

@app.route("/borrar_datos", methods=["POST"])
@cross_origin()
def borrar_datos():
    datos = request.json
    clave = datos.get("clave")
    if clave != "@@ADMIN123@@":
        return jsonify({"error": "Clave incorrecta"}), 403

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        return jsonify({"mensaje": "✅ Datos borrados correctamente."})
    else:
        return jsonify({"mensaje": "No hay datos guardados."})

@app.route("/borrar_usuario", methods=["POST"])
@cross_origin()
def borrar_usuario():
    datos = request.json
    clave = datos.get("clave")
    marca = datos.get("marca")

    if clave != "@@ADMIN123@@":
        return jsonify({"error": "Clave incorrecta"}), 403

    if not marca:
        return jsonify({"error": "Falta la marca del usuario"}), 400

    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            lista_datos = json.load(f)

        nueva_lista = [item for item in lista_datos if item.get("marca") != marca]

        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(nueva_lista, f, indent=4, ensure_ascii=False)

        return jsonify({"mensaje": f"✅ Usuario con marca '{marca}' borrado correctamente."})
    else:
        return jsonify({"mensaje": "No hay datos guardados."})

if __name__ == "__main__":
    app.run(debug=True)
