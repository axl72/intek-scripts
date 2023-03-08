import argparse
from clientes import Cliente
from sendmail import MailSender
import masterpath
import re


lista_clientes = {23: Cliente(23, "Tiendas Peruanas", "dte_20493020618@paperless.pe", ruc="204930206180"), 22:
                  Cliente(22, "Tiendas Peruanas Oriente",
                          "dte_20600414276@paperless.pe", ruc="20600414276"),
                  15: Cliente(15, "Hipermercados Tottus",
                              "dte_20508565934@paperless.pe", ruc="20508565934"),
                  74: Cliente(74, "Hipermercados Tottus Oriente",
                              "dte_20393864886@paperless.pe", ruc="20393864886"),
                  13: Cliente(13, "Estilos", "facturas@estilos.com.pe",
                              ruc="20100199158"),
                  20: Cliente(20, "Happyland", "ventanilla.facturas@happyland.pe",
                              ruc="20342062521"),
                  4: Cliente(4, "Coney Park", "facturacionelectronica@coneypark.com", ruc="20600768043"),
                  -1: Cliente(-1, "Axell Bernabel", "axell.bernabel@unmsm.edu.pe", dni="71269132")}


def enviar_factura(remitente: str, cliente: Cliente, codigo_comprobante, asunto, texto, adjunto, nombre):
    # plaintext = texto
    correo = cliente.email
    ourmailsender = MailSender(
        'axell.bernabel@intektoys.com', 'rCKLANx+Ab', ('smtp.gmail.com', 587))
    html = texto
    ourmailsender.set_message(plaintext, asunto,
                              remitente, html, adjunto, nombre)
    ourmailsender.set_recipients(["axell.bernabel@unmsm.edu.pe"])
    ourmailsender.connect()
    ourmailsender.send_all()


def obtener_xml(db_path, cod_comprobante: str):
    lista_xml = list(filter(lambda x: x.endswith(
        ".XML"), masterpath.get_listdir(db_path)))
    for xml in lista_xml:
        if re.search(cod_comprobante, xml):
            return xml


if __name__ == "__main__":
    comprobante = obtener_xml(
        "G:\\1.USUARIOS\\FACTURACION\\COMPROBANTES", "F101-00002795")
    print(comprobante)
    input()

    parser = argparse.ArgumentParser()
    parser.add_argument("cliente")
    parser.add_argument("codigo_comprobante")
    argumentos = parser.parse_args()
    plaintext = "Hola viejo como estás"
    asunto = "FACTURA INTEK MARZO"
    remitente = "Axell Bernabel"
    adjunto = "example.txt"
    enviar_factura(remitente, lista_clientes[-1],
                   argumentos.codigo_comprobante, asunto, plaintext, adjunto, adjunto)
