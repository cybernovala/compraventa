from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io

def crear_pdf(texto):
    # Separar líneas del texto completo
    lineas = texto.strip().split("\n")

    # Extraer secciones
    titulo = "CONTRATO DE COMPRAVENTA DE VEHÍCULO"
    fecha = lineas[1].strip() if len(lineas) > 1 else ""

    # Cuerpo del contrato: desde línea 2 hasta las últimas 4
    cuerpo = "\n".join(lineas[2:-4]).strip()

    # Pie de firma (últimas 4 líneas)
    firma_vendedor = lineas[-4].strip()
    rut_vendedor = lineas[-3].strip()
    firma_comprador = lineas[-2].strip()
    rut_comprador = lineas[-1].strip()

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título
    pdf.set_font("Arial", "B", 22)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    # Cuerpo
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, cuerpo, align="J")

    # Espacio antes de firmas
    pdf.ln(25)

    # Firmas centradas con línea horizontal
    pdf.set_font("Arial", "", 12)

    # Firma vendedor
    pdf.cell(0, 10, "_____________________________", ln=True, align="C")
    pdf.cell(0, 10, firma_vendedor, ln=True, align="C")
    pdf.cell(0, 10, rut_vendedor, ln=True, align="C")

    pdf.ln(20)

    # Firma comprador
    pdf.cell(0, 10, "_____________________________", ln=True, align="C")
    pdf.cell(0, 10, firma_comprador, ln=True, align="C")
    pdf.cell(0, 10, rut_comprador, ln=True, align="C")

    # Generar PDF en memoria
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Encriptar PDF
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(user_password="@@1234@@", owner_password="@@1234@@")

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_b_
