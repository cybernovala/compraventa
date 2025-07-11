function vistaPrevia() {
  const datos = recogerDatos();
  const texto = generarTextoContrato(datos);

  const preview = document.getElementById("preview");
  preview.style.display = "block";
  preview.innerText = texto;
}

function recogerDatos() {
  return {
    fecha: document.getElementById("fecha").value,
    nombre_vendedor: document.getElementById("nombre_vendedor").value,
    rut_vendedor: document.getElementById("rut_vendedor").value,
    domicilio_vendedor: document.getElementById("domicilio_vendedor").value,
    telefono_vendedor: document.getElementById("telefono_vendedor").value,
    nombre_comprador: document.getElementById("nombre_comprador").value,
    rut_comprador: document.getElementById("rut_comprador").value,
    domicilio_comprador: document.getElementById("domicilio_comprador").value,
    telefono_comprador: document.getElementById("telefono_comprador").value,
    marca: document.getElementById("marca").value,
    modelo: document.getElementById("modelo").value,
    anio: document.getElementById("anio").value,
    vin: document.getElementById("vin").value,
    patente: document.getElementById("patente").value,
    color: document.getElementById("color").value,
    otros: document.getElementById("otros").value,
    monto: document.getElementById("monto").value,
    forma_pago: document.getElementById("forma_pago").value
  };
}

function generarTextoContrato(datos) {
  return `
CONTRATO DE COMPRAVENTA DE VEHÍCULO

EN LOS ÁNGELES A ${datos.fecha.toUpperCase()}

COMPARECEN:

1. VENDEDOR:
NOMBRE: ${datos.nombre_vendedor.toUpperCase()}
RUT: ${datos.rut_vendedor.toUpperCase()}
DOMICILIO: ${datos.domicilio_vendedor.toUpperCase()}
TELÉFONO: ${datos.telefono_vendedor.toUpperCase()}

2. COMPRADOR:
NOMBRE: ${datos.nombre_comprador.toUpperCase()}
RUT: ${datos.rut_comprador.toUpperCase()}
DOMICILIO: ${datos.domicilio_comprador.toUpperCase()}
TELÉFONO: ${datos.telefono_comprador.toUpperCase()}

... (se verán todas las cláusulas en el PDF final)
`.toUpperCase();
}

async function generarPDF() {
  const datos = recogerDatos();

  const response = await fetch("https://compraventa-5lhy.onrender.com/generar_pdf", {
    method: "POST",
    body: JSON.stringify(datos),
    headers: { "Content-Type": "application/json" }
  });

  const pdfBlob = await response.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(pdfBlob);
  link.download = "contrato_compraventa_cybernova.pdf";
  link.click();
}
