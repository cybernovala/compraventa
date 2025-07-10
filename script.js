function vistaPrevia() {
  const datos = recogerDatos();
  const texto = `
CONTRATO DE COMPRAVENTA DE VEHÍCULO

${datos.fecha.toUpperCase()}

COMPARECEN:

1. Vendedor:
Nombre: ${datos.nombre_vendedor}
RUT: ${datos.rut_vendedor}
Domicilio: ${datos.domicilio_vendedor}
Teléfono: ${datos.telefono_vendedor}

2. Comprador:
Nombre: ${datos.nombre_comprador}
RUT: ${datos.rut_comprador}
Domicilio: ${datos.domicilio_comprador}
Teléfono: ${datos.telefono_comprador}

Ambas partes acuerdan celebrar el presente contrato, bajo las siguientes cláusulas:

PRIMERA: Objeto del contrato
Marca: ${datos.marca}
Modelo: ${datos.modelo}
Año: ${datos.anio}
VIN: ${datos.vin}
Patente: ${datos.patente}
Color: ${datos.color}
Otros: ${datos.otros}

SEGUNDA: Precio y forma de pago
Monto: ${datos.monto}
Forma de pago: ${datos.forma_pago}

(El resto de las cláusulas y firmas se completan en el PDF final.)
`.toUpperCase();

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

async function generarPDF() {
  const datos = recogerDatos();
  const texto = `
CONTRATO DE COMPRAVENTA DE VEHÍCULO

${datos.fecha.toUpperCase()}

COMPARECEN:

1. Vendedor:
Nombre: ${datos.nombre_vendedor}
RUT: ${datos.rut_vendedor}
Domicilio: ${datos.domicilio_vendedor}
Teléfono: ${datos.telefono_vendedor}

2. Comprador:
Nombre: ${datos.nombre_comprador}
RUT: ${datos.rut_comprador}
Domicilio: ${datos.domicilio_comprador}
Teléfono: ${datos.telefono_comprador}

PRIMERA: Objeto
Marca: ${datos.marca}
Modelo: ${datos.modelo}
Año: ${datos.anio}
VIN: ${datos.vin}
Patente: ${datos.patente}
Color: ${datos.color}
Otros: ${datos.otros}

SEGUNDA: Precio y forma de pago
Monto: ${datos.monto}
Forma de pago: ${datos.forma_pago}

${datos.nombre_vendedor}
${datos.rut_vendedor}
${datos.nombre_comprador}
${datos.rut_comprador}
`.toUpperCase();

  const response = await fetch("https://compraventa-5lhy.onrender.com/generar_pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ contenido: texto })
  });

  const pdfBlob = await response.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(pdfBlob);
  link.download = "contrato_compraventa_cybernova.pdf";
  link.click();
}
