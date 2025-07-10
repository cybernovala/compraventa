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
    marca_usuario: document.getElementById("marca").value || "usuario_compraventa", // 👈 corregido aquí
    marca_vehiculo: document.getElementById("marca").value,
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

Ambas partes acuerdan celebrar el presente contrato de compraventa de vehículo, de acuerdo a las siguientes cláusulas:

PRIMERA: Objeto del contrato
El vendedor se compromete a vender al comprador, quien compra en este acto, el vehículo de características siguientes:

Marca: ${datos.marca_vehiculo}
Modelo: ${datos.modelo}
Año de fabricación: ${datos.anio}
Número de serie (VIN): ${datos.vin}
Patente: ${datos.patente}
Color: ${datos.color}
Otros: ${datos.otros}

SEGUNDA: Precio y forma de pago
El precio total de la compraventa es de ${datos.monto}, que el comprador pagará al vendedor de la siguiente forma:
${datos.forma_pago}

TERCERA: Entrega del vehículo
El vendedor se compromete a entregar el vehículo al comprador en el estado que se encuentra, en el domicilio del vendedor o en otro lugar acordado.

CUARTA: Declaraciones del vendedor
El vendedor declara que:
- Es propietario del vehículo.
- El vehículo no tiene gravámenes, multas ni embargos.
- Cuenta con documentos legales vigentes.

${datos.nombre_vendedor}
${datos.rut_vendedor}
${datos.nombre_comprador}
${datos.rut_comprador}
`.toUpperCase();
}

async function generarPDF() {
  const datos = recogerDatos();
  const texto = generarTextoContrato(datos);

  const payload = {
    contenido: texto,
    marca_usuario: datos.marca_usuario // 👈 corregido
  };

  const response = await fetch("https://curriculum-9s9x.onrender.com/generar_pdf", {
    method: "POST",
    body: JSON.stringify(payload),
    headers: { "Content-Type": "application/json" }
  });

  const pdfBlob = await response.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(pdfBlob);
  link.download = "contrato_compraventa_cybernova.pdf";
  link.click();
}
