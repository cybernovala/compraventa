from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io

def crear_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, texto, align="J")

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    # Agregar contraseña
    reader = PdfReader(pdf_buffer)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(user_password="@@1234@@", owner_password="@@1234@@")

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()
