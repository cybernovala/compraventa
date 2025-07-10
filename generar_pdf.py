from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

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

    # Marca de agua si no es admin
    if not admin:
        pdf.set_text_color(200, 200, 200)
        pdf.set_font("Arial", "B", 50)
        pdf.rotate(45, x=pdf.w / 2, y=pdf.h / 2)
        pdf.text(x=pdf.w / 2 - 60, y=pdf.h / 2, txt="CYBERNOVA")
        pdf.rotate(0)

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output

# Función para rotar texto
def rotate(self, angle, x=None, y=None):
    if x is None:
        x = self.x
    if y is None:
        y = self.y
    self._out(f'q {self._get_rotation_matrix(angle, x, y)} cm')

def _get_rotation_matrix(self, angle, x, y):
    angle_rad = angle * 3.14159265 / 180
    c = round(cos(angle_rad), 5)
    s = round(sin(angle_rad), 5)
    return f"{c} {s} {-s} {c} {x} {y}"

PDF.rotate = rotate
PDF._get_rotation_matrix = _get_rotation_matrix
