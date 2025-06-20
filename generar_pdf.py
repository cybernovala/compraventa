from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io

def crear_pdf(texto):
    # Crear el PDF en memoria
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, texto, align="J")

    # Obtener el PDF como bytes
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Leer los bytes con PyPDF2
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Agregar contraseña
    writer.encrypt(user_password="@@1234@@", owner_password="@@1234@@")

    # Guardar el resultado en memoria y devolverlo
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)

    return output_buffer.read()
