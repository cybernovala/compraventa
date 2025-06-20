from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io
import re

class PDF(FPDF):
    def write_bold_text(self, text, regular_font="Arial", regular_size=12):
        """
        Escribe texto con los subtítulos en negrita.
        """
        lines = text.split("\n")
        for line in lines:
            if re.match(r"^\s*(PRIMERA|SEGUNDA|TERCERA|CUARTA|QUINTA|SEXTA|SÉPTIMA|OCTAVA|NOVENA|Comparecen|1\.|2\.).*", line):
                self.set_font(regular_font, "B", regular_size)
            elif ":" in line:
                self.set_font(regular_font, "B", regular_size)
            else:
                self.set_font(regular_font, "", regular_size)
            self.multi_cell(0, 10, line, align="J")

def crear_pdf(texto):
    # Separar líneas del texto completo
    lineas = [line.strip() for line in texto.strip().split("\n") if line.strip()]

    if len(lineas) < 6:
        raise ValueError("El texto no contiene suficientes líneas para generar el contrato.")

    # Extraer secciones
    titulo = "CONTRATO DE COMPRAVENTA DE VEHÍCULO"
    fecha = lineas[1]
    cuerpo = "\n".join(lineas[2:-4]).strip()

    firma_vendedor = lineas[-4]
    rut_vendedor = lineas[-3]
    firma_comprador = lineas[-2]
    rut_comprador = lineas[-1]

    # Crear PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título centrado, negrita, grande (20)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha alineada a la derecha
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    # Cuerpo del contrato con estilos
    pdf.write_bold_text(cuerpo)

    # Espacio antes de firmas
    pdf.ln(25)

    # Firmas: columnas alineadas
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width / 2
    y = pdf.get_y()

    pdf.set_y(y)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 8, "_____________________________", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 8, "_____________________________", 0, 1, "C")

    pdf.set_font("Arial", "B", 12)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, firma_vendedor, 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, firma_comprador, 0, 1, "C")

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
