from fpdf import FPDF
import io

def crear_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "", 12)

    # Marca de agua
    pdf.set_text_color(200, 200, 200)
    pdf.set_font("Arial", "B", 50)
    pdf.rotate(45, x=None, y=None)
    pdf.text(40, 180, "CYBERNOVA")
    pdf.rotate(0)

    # Texto principal
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, texto, align="J")

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return pdf_bytes
