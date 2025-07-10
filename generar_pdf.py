from fpdf import FPDF
import io

def crear_pdf(texto):
    lineas = [line.strip() for line in texto.strip().split("\n") if line.strip()]

    if len(lineas) < 6:
        raise ValueError("El texto no contiene suficientes líneas para generar el contrato.")

    titulo = "CONTRATO DE COMPRAVENTA DE VEHÍCULO"
    fecha = lineas[1]
    cuerpo_lineas = lineas[2:-4]
    firma_vendedor = lineas[-4]
    rut_vendedor = lineas[-3]
    firma_comprador = lineas[-2]
    rut_comprador = lineas[-1]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    # Cuerpo
    pdf.set_font("Arial", "", 11)
    for linea in cuerpo_lineas:
        pdf.multi_cell(0, 9, linea, align="J")
        pdf.ln(1)

    # Espacio para firmas
    pdf.ln(25)
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width / 2
    y = pdf.get_y()

    pdf.set_y(y)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 8, "_____________________________", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 8, "_____________________________", 0, 1, "C")

    pdf.set_font("Arial", "B", 11)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, firma_vendedor, 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, firma_comprador, 0, 1, "C")

    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, f"RUT: {rut_vendedor}", 0, 0, "C")
    pdf.set_x(pdf.l_margin + col_width)
    pdf.cell(col_width, 7, f"RUT: {rut_comprador}", 0, 1, "C")

    # Agregar marca de agua "CYBERNOVA"
    pdf.set_font("Arial", "B", 50)
    pdf.set_text_color(200, 200, 200)
    pdf.rotate(45, x=None, y=None)
    pdf.text(35, 200, "CYBERNOVA")
    pdf.rotate(0)

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return pdf_bytes
