from fpdf import FPDF
from math import radians, cos, sin

class PDF(FPDF):
    def watermark(self, text):
        self.set_text_color(200, 200, 200)
        self.set_font("Arial", "I", 50)
        self.rotate(45, x=self.w / 2, y=self.h / 2)
        self.text(x=self.w / 2 - 60, y=self.h / 2, txt=text)
        self.rotate(0)

    def rotate(self, angle, x=None, y=None):
        if self.angle != 0:
            self._out('Q')
        self.angle = angle
        if angle != 0:
            x = x if x is not None else self.x
            y = y if y is not None else self.y
            angle_rad = radians(angle)
            c = cos(angle_rad)
            s = sin(angle_rad)
            cx = x * self.k
            cy = (self.h - y) * self.k
            self._out(f'q {c:.5f} {s:.5f} {-s:.5f} {c:.5f} {cx - c * cx - s * cy:.5f} {cy - c * cy + s * cx:.5f} cm')
        else:
            self._out('Q')

    def _endpage(self):
        if self.angle != 0:
            self.angle = 0
            self._out('Q')
        super()._endpage()

def generar_pdf_compraventa(data, admin=False):
    pdf = PDF()
    pdf.angle = 0
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "CONTRATO DE COMPRAVENTA DE VEHÍCULO", ln=True, align="C")

    # Fecha alineada a la derecha
    fecha = data.get("fecha", "")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, fecha.upper(), ln=True, align="R")
    pdf.ln(5)

    # Contenido
    contenido = data.get("contenido", "")
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 7, contenido)

    # Espacio para firmas
    pdf.ln(15)

    pdf.cell(80, 10, "_" * 30, ln=0, align="C")
    pdf.cell(30, 10, "", ln=0)
    pdf.cell(80, 10, "_" * 30, ln=1, align="C")

    nombre_vendedor = data.get("nombre_vendedor", "")
    nombre_comprador = data.get("nombre_comprador", "")
    rut_vendedor = data.get("rut_vendedor", "")
    rut_comprador = data.get("rut_comprador", "")

    pdf.cell(80, 7, nombre_vendedor, ln=0, align="C")
    pdf.cell(30, 7, "", ln=0)
    pdf.cell(80, 7, nombre_comprador, ln=1, align="C")
    pdf.cell(80, 7, f"RUT: {rut_vendedor}", ln=0, align="C")
    pdf.cell(30, 7, "", ln=0)
    pdf.cell(80, 7, f"RUT: {rut_comprador}", ln=1, align="C")

    # Marca de agua
    if not admin:
        pdf.watermark("NOVANOVA")

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output
