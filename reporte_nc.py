import os
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook


def get_nc(filepath):
    pascal_file = open(filepath)
    pascal_contents = pascal_file.read()
    soup = BeautifulSoup(pascal_contents, "xml")
    id = soup.find("cbc:ID").text
    fecha = soup.find("cbc:IssueDate").text
    doc_ref = soup.find("cac:DiscrepancyResponse")
    id_doc_ref = doc_ref.find("cbc:ReferenceID").text
    description = doc_ref.find("cbc:Description").text
    dni_ruc = soup.find("cac:AccountingCustomerParty").find(
        "cac:Party").find("cac:PartyIdentification").find("cbc:ID").text
    nombre_cliente = soup.find("cac:AccountingCustomerParty").find(
        "cac:Party").find("cac:PartyLegalEntity").find("cbc:RegistrationName").text
    igv = soup.find("cac:TaxTotal").find("cbc:TaxAmount").text
    valor_venta = soup.find("cac:LegalMonetaryTotal").find(
        "cbc:LineExtensionAmount").text
    total = soup.find("cbc:TaxInclusiveAmount").text

    row = [id, fecha, id_doc_ref, description, dni_ruc,
           nombre_cliente, valor_venta, igv, total]
    return row


def get_files(path):
    files = os.listdir(path)
    files = [os.path.join(path, file)
             for file in files if file.endswith(".XML")]
    return files


def get_matrix_nc(path):
    files = get_files(path)
    matrix = [get_nc(file) for file in files]
    return matrix


def generar_reporte(year=2023):
    save_name = f"REPORTE-{year}.xlsx"
    matrix = get_matrix_nc(
        f"G:\\1.USUARIOS\\FACTURACION\\NOTAS DE CREDITO\\{year}")
    matrix.insert(0, ["ID NOTA DE CREDITO", "FECHA DE EMISION", "COD. REFERENCIA",
                      "GLOSA", "DNI/RUC", "CLIENTE", "VALOR", "IGV", "TOTAL"])
    wb = Workbook()
    ws = wb.active
    ws.title = "NC"
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            ws.cell(row=1+i, column=j+1).value = matrix[i][j]

    wb.save(save_name)
    print("Reporte generado exitosamente")


if __name__ == "__main__":
    generar_reporte()
