from fpdf import FPDF
import io

def crear_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Marca de agua CYBERNOVA
    pdf.set_font("Arial", "B", 50)
    pdf.set_text_color(220, 220, 220)
    pdf.rotate(45, x=None, y=None)
    pdf.text(30, 200, "CYBERNOVA")
    pdf.rotate(0)

    # Contenido principal
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 9, texto, align="J")

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return pdf_bytes
