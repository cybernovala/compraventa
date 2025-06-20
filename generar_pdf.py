from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io

def crear_pdf(texto):
    # Separar fecha y cuerpo del texto
    lineas = texto.strip().split("\n", 2)
    titulo = "CONTRATO DE COMPRAVENTA DE VEHÍCULO"
    fecha = lineas[1].strip() if len(lineas) > 1 else ""
    cuerpo = lineas[2].strip() if len(lineas) > 2 else texto.strip()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título centrado, negrita, tamaño 28
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha alineada a la derecha
    pdf.set_font("Arial", "", 14)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    # Cuerpo del contrato, justificado
    lineas = texto.strip().split("\n", 2)
    pdf.set_font("Arial", "", 14)
    pdf.multi_cell(0, 10, cuerpo, align="J")

    # Convertir a bytes para encriptar
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # Contraseña
    writer.encrypt(user_password="@@1234@@", owner_password="@@1234@@")

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()
