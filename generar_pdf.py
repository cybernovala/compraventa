import io
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter

def generar_pdf_curriculum(data, admin=False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "CURRICULUM VITAE", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 14)
    nombre = data.get("nombre", "")
    rut = data.get("rut", "")
    pdf.cell(0, 10, f"Nombre: {nombre}", ln=True)
    pdf.cell(0, 10, f"RUT: {rut}", ln=True)

    if not admin:
        pdf.set_text_color(150, 150, 150)
        pdf.set_font("Arial", "I", 30)
        pdf.set_xy(20, 250)
        pdf.cell(0, 10, "CYBERNOVA", align="C")

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output

def generar_pdf_compraventa(data, admin=False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "CONTRATO DE COMPRAVENTA", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 14)
    contenido = data.get("contenido", "")
    pdf.multi_cell(0, 10, contenido)

    if not admin:
        pdf.set_text_color(150, 150, 150)
        pdf.set_font("Arial", "I", 30)
        pdf.set_xy(20, 250)
        pdf.cell(0, 10, "CYBERNOVA", align="C")

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output
