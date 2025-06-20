from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io
import re

def crear_pdf(texto):
    lineas = [line.strip() for line in texto.strip().split("\n") if line.strip()]

    if len(lineas) < 6:
        raise ValueError("El texto no contiene suficientes líneas para generar el contrato.")

    titulo = "CONTRATO DE COMPRAVENTA DE VEHÍCULO"
    fecha = lineas[1]
    cuerpo_lineas = lineas[2:-4]
    firma_vendedor = lineas[-4]
    rut_vendedor = lineas[-3]
    firma_comprador = lineas[-2]
    rut_comprador = lineas[-1]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    clausula_3_detectada = False
    for linea in cuerpo_lineas:
        texto_mayus = linea.upper()

        # Detectar inicio de cláusulas para espacio extra
        clausulas_iniciales = [
            "COMPARECEN:", "PRIMERA:", "SEGUNDA:", "TERCERA:", "CUARTA:", "QUINTA:",
            "SEXTA:", "SÉPTIMA:", "OCTAVA:", "NOVENA:", "DÉCIMA:"
        ]
        if any(texto_mayus.startswith(clausula) for clausula in clausulas_iniciales):
            pdf.ln(5)

        # Saltos personalizados
        if texto_mayus == "COMPARECEN:":
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 9, linea.strip(), ln=True)
            pdf.ln(3)
            continue

        if texto_mayus.startswith("2. COMPRADOR:"):
            pdf.ln(3)
        if texto_mayus.startswith("AMBAS PARTES ACUERDAN"):
            pdf.ln(3)
        if texto_mayus.startswith("VEHÍCULO DE CARACTERÍSTICAS SIGUIENTES:"):
            pdf.ln(3)
        if texto_mayus.startswith("OTROS:"):
            pass
        if texto_mayus.startswith("SEGUNDA:"):
            pdf.ln(3)
        if not clausula_3_detectada and "TERCERA" in texto_mayus:
            clausula_3_detectada = True

        # OBJETO DEL CONTRATO
        if "OBJETO DEL CONTRATO" in texto_mayus:
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 9, linea, align="J")
            continue

        # PRECIO Y FORMA DE PAGO con monto en negrita
        if "PRECIO Y FORMA DE PAGO" in texto_mayus and "$" in linea:
            pdf.set_font("Arial", "", 11)
            match = re.search(r'(\$\s?\d[\d\.\s]*)', linea)
            if match:
                inicio, fin = match.span()
                antes = linea[:inicio]
                monto = match.group(1).strip()
                despues = linea[fin:]

                pdf.set_font("Arial", "", 11)
                pdf.write(5, antes)

                pdf.set_font("Arial", "B", 11)
                pdf.write(5, monto + " ")

                pdf.set_font("Arial", "", 11)
                pdf.write(5, despues + "\n")
            else:
                pdf.multi_cell(0, 9, linea, align="J")
            continue

        # Negrita para datos antes de cláusula 3
        if (not clausula_3_detectada and ':' in linea and
            "PRECIO Y FORMA DE PAGO" not in texto_mayus and
            "OBJETO DEL CONTRATO" not in texto_mayus):
            parte1, parte2 = linea.split(':', 1)
            pdf.set_font("Arial", "", 11)
            pdf.write(5, f"{parte1.strip()}: ")
            pdf.set_font("Arial", "B", 11)
            pdf.write(5, f"{parte2.strip()}\n")
        else:
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 9, linea, align="J")

    # Firmas
    pdf.ln(25)
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width / 2
    y = pdf.get_y()

    pdf.set_y(y)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 8, "_____________________________", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 8, "_____________________________", 0, 1, "C")

    pdf.set_font("Arial", "B", 11)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, firma_vendedor, 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, firma_comprador, 0, 1, "C")

    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, f"RUT: {rut_vendedor}", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, f"RUT: {rut_comprador}", 0, 1, "C")

    # Encriptar PDF
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(user_password="@@1234@@", owner_password="@@1234@@")

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()
