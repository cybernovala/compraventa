from fpdf import FPDF
import io

class PDF(FPDF):
    def rotate(self, angle, x=None, y=None):
        # Rotación para la marca de agua
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        self._out(f'q {self._get_rotation_matrix(angle, x, y)}')

    def _get_rotation_matrix(self, angle, x, y):
        angle = angle * 3.14159265 / 180
        c = round(np.cos(angle), 5)
        s = round(np.sin(angle), 5)
        return f'{c} {s} {-s} {c} {x * self.k} {y * self.k} cm'

    def _endpage(self):
        self._out('Q')
        super()._endpage()

def crear_pdf(texto, admin=False):
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

    # Marca de agua si no es admin
    if not admin:
        pdf.set_font("Arial", "B", 50)
        pdf.set_text_color(200, 200, 200)
        pdf.rotate(45, x=60, y=60)
        pdf.text(60, 60, "CYBERNOVA")
        pdf.rotate(0)

    # Título
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, titulo, ln=True, align="C")

    # Fecha
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, fecha, ln=True, align="R")
    pdf.ln(5)

    for linea in cuerpo_lineas:
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 9, linea, align="J")

    # Firmas
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

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return pdf_bytes
