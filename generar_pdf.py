from fpdf import FPDF
from math import cos, sin, radians

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def rotate(self, angle, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        self._out(f'q {self._get_rotation_matrix(angle, x, y)} cm')

    def _get_rotation_matrix(self, angle, x, y):
        angle_rad = radians(angle)
        c = cos(angle_rad)
        s = sin(angle_rad)
        return f"{c:.5f} {s:.5f} {-s:.5f} {c:.5f} {x:.2f} {y:.2f}"

    def reset_rotation(self):
        self._out("Q")

def generar_pdf_compraventa(data, admin=False):
    pdf = PDF()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "CONTRATO DE COMPRAVENTA DE VEHÍCULO", ln=True, align="C")

    # Fecha alineada derecha
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, data.get("fecha", ""), ln=True, align="R")
    pdf.ln(5)

    # Contenido
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, data.get("contenido", ""), align="J")
    pdf.ln(20)

    # Firmas
    pdf.cell(80, 8, "_____________________________", ln=0, align="C")
    pdf.cell(30, 8, "", ln=0)
    pdf.cell(80, 8, "_____________________________", ln=1, align="C")

    pdf.cell(80, 8, data.get("nombre_vendedor", ""), ln=0, align="C")
    pdf.cell(30, 8, "", ln=0)
    pdf.cell(80, 8, data.get("nombre_comprador", ""), ln=1, align="C")

    pdf.cell(80, 8, f"RUT: {data.get('rut_vendedor', '')}", ln=0, align="C")
    pdf.cell(30, 8, "", ln=0)
    pdf.cell(80, 8, f"RUT: {data.get('rut_comprador', '')}", ln=1, align="C")

    # Marca de agua
    if not admin:
        pdf.set_text_color(220, 220, 220)
        pdf.set_font("Arial", "B", 50)
        pdf.rotate(45, x=pdf.w / 2, y=pdf.h / 2)
        pdf.text(x=pdf.w / 2 - 60, y=pdf.h / 2, txt="CYBERNOVA")
        pdf.reset_rotation()

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output
