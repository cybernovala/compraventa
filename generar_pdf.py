from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io

def crear_pdf(texto):
    # Separar líneas del texto completo
    lineas = texto.strip().split("\n")

    # Extraer secciones
    titulo = "CONTRATO DE COMPRAVENTA DE VEHÍCULO"
    fecha = lineas[1].strip() if len(lineas) > 1 else ""
    cuerpo = "\n".join(lineas[2:-4]).strip()
    firma_vendedor = lineas[-4].strip()
    rut_vendedor = lineas[-3].strip()
    firma_comprador = lineas[-2].strip()
    rut_comprador = lineas[-1].strip()

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título centrado, negrita, grande
    pdf.set_font("Arial", "B", 22)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha alineada a la derecha
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    # Cuerpo del contrato justificado
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, cuerpo, align="J")

    # Espacio antes de firmas
    pdf.ln(20)

    # Pie de firma del VENDEDOR (alineado y compacto)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "_____________________________", ln=True, align="C")
    pdf.cell(0, 6, firma_vendedor, ln=True, align="C")
    pdf.cell(0, 6, f"RUT: {rut_vendedor}", ln=True, align="C")

    # Espacio entre firmas
    pdf.ln(15)

    # Pie de firma del COMPRADOR (alineado y compacto)
    pdf.cell(0, 8, "_____________________________", ln=True, align="C")
    pdf.cell(0, 6, firma_comprador, ln=True, align="C")
    pdf.cell(0, 6, f"RUT: {rut_comprador}", ln=True, align="C")

    # Exportar el PDF a bytes
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
