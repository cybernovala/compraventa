from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io
import re

def crear_pdf(texto):
    # Separar líneas del texto completo
    lineas = [line.strip() for line in texto.strip().split("\n") if line.strip()]

    # Validar longitud mínima
    if len(lineas) < 6:
        raise ValueError("El texto no contiene suficientes líneas para generar el contrato.")

    # Extraer secciones
    titulo = "CONTRATO DE COMPRAVENTA DE VEHÍCULO"
    fecha = lineas[1]
    cuerpo_lineas = lineas[2:-4]
    firma_vendedor = lineas[-4]
    rut_vendedor = lineas[-3]
    firma_comprador = lineas[-2]
    rut_comprador = lineas[-1]

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título centrado, negrita, grande
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha alineada a la derecha (tamaño 11)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    # Cuerpo del contrato justificado (tamaño 11)
    for linea in cuerpo_lineas:
        if ':' in linea:
            partes = linea.split(':', 1)
            campo = partes[0].strip()
            valor = partes[1].strip()

            # Escribir campo normal
            pdf.set_font("Arial", "", 11)
            pdf.write(5, f"{campo}: ")

            # Escribir valor en negrita
            pdf.set_font("Arial", "B", 11)
            pdf.write(5, f"{valor}\n")
        else:
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 9, linea, align="J")

    # Espacio antes de firmas
    pdf.ln(25)

    # Pie de firma: en columnas alineadas
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width / 2
    y = pdf.get_y()

    # Línea para firmas
    pdf.set_y(y)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 8, "_____________________________", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 8, "_____________________________", 0, 1, "C")

    # Nombres (solo los datos ingresados en negrita)
    pdf.set_font("Arial", "B", 11)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, firma_vendedor, 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, firma_comprador, 0, 1, "C")

    # RUTs (solo valores en negrita)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, f"RUT: {rut_vendedor}", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, f"RUT: {rut_comprador}", 0, 1, "C")

    # Exportar PDF como bytes
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Encriptar PDF
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(user_password="@@1234@@", owner_password="@@1234@@")

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()
