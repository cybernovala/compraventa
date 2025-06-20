function vistaPrevia() {
  const datos = recogerDatos();
  const texto = `
CONTRATO DE COMPRAVENTA DE VEHÍCULO

${datos.fecha.toUpperCase()}

Comparecen:

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

Marca: ${datos.marca}
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

EL RESTO DE LAS CLÁUSULAS Y EL PIE DE FIRMA APARECEN EN EL PDF FINAL...
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
  const contenido = `
CONTRATO DE COMPRAVENTA DE VEHÍCULO

${document.getElementById("fecha").value.toUpperCase()}

Comparecen:

1. Vendedor:
Nombre: ${document.getElementById("nombre_vendedor").value}
RUT: ${document.getElementById("rut_vendedor").value}
Domicilio: ${document.getElementById("domicilio_vendedor").value}
Teléfono: ${document.getElementById("telefono_vendedor").value}

2. Comprador:
Nombre: ${document.getElementById("nombre_comprador").value}
RUT: ${document.getElementById("rut_comprador").value}
Domicilio: ${document.getElementById("domicilio_comprador").value}
Teléfono: ${document.getElementById("telefono_comprador").value}

Ambas partes acuerdan celebrar el presente contrato de compraventa de vehículo, de acuerdo a las siguientes cláusulas:

PRIMERA: Objeto del contrato
El vendedor se compromete a vender al comprador, quien compra en este acto, el vehículo de características siguientes:

Marca: ${document.getElementById("marca").value}
Modelo: ${document.getElementById("modelo").value}
Año de fabricación: ${document.getElementById("anio").value}
Número de serie (VIN): ${document.getElementById("vin").value}
Patente: ${document.getElementById("patente").value}
Color: ${document.getElementById("color").value}
Otros: ${document.getElementById("otros").value}

SEGUNDA: Precio y forma de pago
El precio total de la compraventa es de ${document.getElementById("monto").value}, que el comprador pagará al vendedor de la siguiente forma:
${document.getElementById("forma_pago").value}

TERCERA: Entrega del vehículo
El vendedor se compromete a entregar el vehículo al comprador en el estado que se encuentra, en el domicilio del vendedor o en otro lugar acordado.

CUARTA: Declaraciones del vendedor
El vendedor declara que:
- Es propietario del vehículo.
- El vehículo no tiene gravámenes, multas ni embargos.
- Cuenta con documentos legales vigentes.

QUINTA: Responsabilidad del vendedor
El vendedor asegura que el vehículo se encuentra en condiciones técnicas adecuadas para su uso, sin defectos ocultos.

SEXTA: Responsabilidad del comprador
El comprador declara haber revisado el vehículo y estar conforme con su estado.

SÉPTIMA: Transferencia de propiedad
Ambas partes acuerdan que, al momento de la entrega del vehículo y el pago total del precio, se procederá al traspaso de propiedad.

OCTAVA: Incumplimiento
En caso de incumplimiento por cualquiera de las partes, se recurrirá a acciones legales.

NOVENA: Jurisdicción y resolución de conflictos
Para efectos legales derivados del contrato, se someten a la jurisdicción de los tribunales de la ciudad.

FIRMAS:

VENDEDOR: ${document.getElementById("nombre_vendedor").value}
                RUT: ${document.getElementById("rut_vendedor").value}

COMPRADOR: ${document.getElementById("nombre_comprador").value}
                   RUT: ${document.getElementById("rut_comprador").value}
`.toUpperCase();

  const blob = new Blob([JSON.stringify({ contenido })], {
    type: "application/json"
  });

  const response = await fetch("https://compraventa-5lhy.onrender.com/generar_pdf", {
    method: "POST",
    body: blob,
    headers: { "Content-Type": "application/json" }
  });

  const pdfBlob = await response.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(pdfBlob);
  link.download = "contrato_compraventa.pdf";
  link.click();
}
