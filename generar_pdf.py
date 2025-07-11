from fpdf import FPDF
import math

class PDF(FPDF):
    def add_watermark(self, text):
        # Guardar posición original
        saved_x = self.x
        saved_y = self.y

        self.set_text_color(200, 200, 200)
        self.set_font("Arial", "I", 50)

        center_x = self.w / 2
        center_y = self.h / 2

        # Calcular ángulo
        angle = 45
        angle_rad = math.radians(angle)
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)

        # Guardar estado gráfico
        self._out("q")

        # Traslación al centro
        self._out(f"1 0 0 1 {center_x * self.k} {(self.h - center_y) * self.k} cm")
        # Rotación
        self._out(f"{c:.5f} {s:.5f} {-s:.5f} {c:.5f} 0 0 cm")
        # Traslación para centrar texto
        self._out("1 0 0 1 -50 0 cm")  # Ajustar horizontal (puedes mover -50 si quieres afinar)

        # Dibujar texto
        self.cell(100, 10, text, align="C")

        # Restaurar estado gráfico
        self._out("Q")

        # Restaurar posición original
        self.set_xy(saved_x, saved_y)


def generar_pdf_compraventa(data, admin=False):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "CONTRATO DE COMPRAVENTA DE VEHÍCULO", ln=True, align="C")
    pdf.ln(5)

    fecha = data.get("fecha", "")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"{fecha.upper()}", ln=True, align="R")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "COMPARECEN:", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 12)
    vendedor = (
        f"1. VENDEDOR:\n"
        f"NOMBRE: {data.get('nombre_vendedor', '').upper()}\n"
        f"RUT: {data.get('rut_vendedor', '').upper()}\n"
        f"DOMICILIO: {data.get('domicilio_vendedor', '').upper()}\n"
        f"TELÉFONO: {data.get('telefono_vendedor', '').upper()}\n"
    )
    pdf.multi_cell(0, 7, vendedor)
    pdf.ln(2)

    comprador = (
        f"2. COMPRADOR:\n"
        f"NOMBRE: {data.get('nombre_comprador', '').upper()}\n"
        f"RUT: {data.get('rut_comprador', '').upper()}\n"
        f"DOMICILIO: {data.get('domicilio_comprador', '').upper()}\n"
        f"TELÉFONO: {data.get('telefono_comprador', '').upper()}\n"
    )
    pdf.multi_cell(0, 7, comprador)
    pdf.ln(2)

    pdf.multi_cell(0, 7, 
        "AMBAS PARTES ACUERDAN CELEBRAR EL PRESENTE CONTRATO DE COMPRAVENTA DE VEHÍCULO, DE ACUERDO A LAS SIGUIENTES CLÁUSULAS:")
    pdf.ln(5)

    clausulas = [
        ("PRIMERA: OBJETO DEL CONTRATO",
         f"EL VENDEDOR SE COMPROMETE A VENDER AL COMPRADOR, QUIEN COMPRA EN ESTE ACTO, EL VEHÍCULO DE CARACTERÍSTICAS SIGUIENTES:\n"
         f"MARCA: {data.get('marca', '').upper()}\n"
         f"MODELO: {data.get('modelo', '').upper()}\n"
         f"AÑO DE FABRICACIÓN: {data.get('anio', '').upper()}\n"
         f"NÚMERO DE SERIE (VIN): {data.get('vin', '').upper()}\n"
         f"PATENTE: {data.get('patente', '').upper()}\n"
         f"COLOR: {data.get('color', '').upper()}\n"
         f"OTROS: {data.get('otros', '').upper()}"),
        ("SEGUNDA: PRECIO Y FORMA DE PAGO",
         f"EL PRECIO TOTAL DE LA COMPRAVENTA ES DE $ {data.get('monto', '').upper()}, QUE EL COMPRADOR PAGARÁ AL VENDEDOR DE LA SIGUIENTE FORMA:\n\n{data.get('forma_pago', '').upper()}"),
        ("TERCERA: ENTREGA DEL VEHÍCULO",
         "EL VENDEDOR SE COMPROMETE A ENTREGAR EL VEHÍCULO AL COMPRADOR EN EL ESTADO QUE SE ENCUENTRA, EN EL DOMICILIO DEL VENDEDOR O EN OTRO LUGAR ACORDADO."),
        ("CUARTA: DECLARACIONES DEL VENDEDOR",
         "- ES PROPIETARIO DEL VEHÍCULO.\n- EL VEHÍCULO NO TIENE GRAVÁMENES, MULTAS NI EMBARGOS.\n- CUENTA CON DOCUMENTOS LEGALES VIGENTES."),
        ("QUINTA: RESPONSABILIDAD DEL VENDEDOR",
         "EL VENDEDOR ASEGURA QUE EL VEHÍCULO SE ENCUENTRA EN CONDICIONES TÉCNICAS ADECUADAS PARA SU USO, SIN DEFECTOS OCULTOS."),
        ("SEXTA: RESPONSABILIDAD DEL COMPRADOR",
         "EL COMPRADOR DECLARA HABER REVISADO EL VEHÍCULO Y ESTAR CONFORME CON SU ESTADO."),
        ("SÉPTIMA: TRANSFERENCIA DE PROPIEDAD",
         "AMBAS PARTES ACUERDAN QUE, AL MOMENTO DE LA ENTREGA DEL VEHÍCULO Y EL PAGO TOTAL DEL PRECIO, SE PROCEDERÁ AL TRASPASO DE PROPIEDAD."),
        ("OCTAVA: INCUMPLIMIENTO",
         "EN CASO DE INCUMPLIMIENTO POR CUALQUIERA DE LAS PARTES, SE RECURRIRÁ A ACCIONES LEGALES."),
        ("NOVENA: JURISDICCIÓN Y RESOLUCIÓN DE CONFLICTOS",
         "PARA EFECTOS LEGALES DERIVADOS DEL CONTRATO, SE SOMETEN A LA JURISDICCIÓN DE LOS TRIBUNALES DE LA CIUDAD.")
    ]

    for titulo, texto in clausulas:
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 7, titulo)
        pdf.ln(1)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 7, texto)
        pdf.ln(3)

    pdf.ln(35)
    pdf.cell(80, 10, "_" * 30, ln=0, align="C")
    pdf.cell(30, 10, "", ln=0)
    pdf.cell(80, 10, "_" * 30, ln=1, align="C")

    pdf.cell(80, 7, data.get('nombre_vendedor', '').upper(), ln=0, align="C")
    pdf.cell(30, 7, "", ln=0)
    pdf.cell(80, 7, data.get('nombre_comprador', '').upper(), ln=1, align="C")

    pdf.cell(80, 7, f"RUT: {data.get('rut_vendedor', '').upper()}", ln=0, align="C")
    pdf.cell(30, 7, "", ln=0)
    pdf.cell(80, 7, f"RUT: {data.get('rut_comprador', '').upper()}", ln=1, align="C")

    # 💧 Colocar la marca de agua al final (o al principio si quieres)
    if not admin:
        pdf.add_watermark("CYBERNOVA")

    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output
