from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io
import re

class PDFContrato(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def add_line_with_bold_value(self, line):
        """
        Detecta si la línea contiene un 'Campo: Valor' y pone el valor en negrita.
        Si no, escribe la línea normal.
        """
        match = re.match(r"^(.*?):\s*(.*)$", line)
        if match:
            campo, valor = match.groups()
            self.set_font("Arial", "", 11)
            self.multi_cell(0, 7, f"{campo}:", align="J")
            self.set_font("Arial", "B", 11)
            self.multi_cell(0, 7, valor, align="J")
        else:
            self.set_font("Arial", "", 11)
            self.multi_cell(0, 7, line, align="J")


def crear_pdf(texto):
    lineas = [line.strip() for line in texto.strip().split("\n") if line.strip()]

    if len(lineas) < 6:
        raise ValueError("El texto no contiene suficientes líneas para generar el contrato.")

    titulo = "CONTRATO DE COMPRAVENTA DE VEHÍCULO"
    fecha = lineas[1]
    cuerpo = lineas[2:-4]
    firma_vendedor = lineas[-4]
    rut_vendedor = lineas[-3]
    firma_comprador = lineas[-2]
    rut_comprador = lineas[-1]

    pdf = PDFContrato()
    pdf.add_page()

    # Título centrado
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha alineada a la derecha
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    # Cuerpo con detección de datos del usuario
    for line in cuerpo:
        pdf.add_line_with_bold_value(line)

    # Espacio antes de firmas
    pdf.ln(25)

    # Firmas en columnas
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width / 2
    y = pdf.get_y()

    pdf.set_y(y)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 8, "_____________________________", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 8, "_____________________________", 0, 1, "C")

    pdf.set_font("Arial", "", 11)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, firma_vendedor, 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, firma_comprador, 0, 1, "C")

    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, f"RUT: {rut_vendedor}", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, f"RUT: {rut_comprador}", 0, 1, "C")

    # Exportar y proteger PDF
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
