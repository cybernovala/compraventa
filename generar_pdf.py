from fpdf import FPDF

class PDF(FPDF):
    def add_watermark(self, text):
        self.set_text_color(200, 200, 200)
        self.set_font("Arial", "I", 50)
        self.rotate(45, x=self.w / 2, y=self.h / 2)
        self.text(self.w / 2 - 60, self.h / 2, text)
        self.rotate(0)

    def rotate(self, angle, x=None, y=None):
        if angle != 0:
            angle_rad = angle * 3.14159265 / 180
            c = round(np.cos(angle_rad), 5)
            s = round(np.sin(angle_rad), 5)
            if x is None:
                x = self.x
            if y is None:
                y = self.y
            cx = x * self.k
            cy = (self.h - y) * self.k
            self._out(f'q {c:.5f} {s:.5f} {-s:.5f} {c:.5f} {cx:.5f} {cy:.5f} cm')
        else:
            self._out('Q')

def generar_pdf_compraventa(data, admin=False):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "CONTRATO DE COMPRAVENTA DE VEHÍCULO", ln=True, align="C")

    # Fecha alineada derecha
    fecha = data.get("fecha", "")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, fecha.upper(), ln=True, align="R")
    pdf.ln(5)

    # Contenido
    contenido = data.get("contenido", "")
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 7, contenido)

    pdf.ln(15)

    # Líneas de firma
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

    # Marca de agua (solo si no es admin)
    if not admin:
        pdf.add_watermark("CYBERNOVA")

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output
