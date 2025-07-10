from fpdf import FPDF
import io

def crear_pdf(texto, admin=False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "CONTRATO DE COMPRAVENTA DE VEHÍCULO", ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, texto, align="J")

    if not admin:
        pdf.set_text_color(200, 200, 200)
        pdf.set_font("Arial", "B", 50)
        pdf.rotate(45, x=None, y=None)
        pdf.text(30, 200, "CYBERNOVA")
        pdf.rotate(0)

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return pdf_bytes
