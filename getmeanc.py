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
    dni_ruc = soup.find("cac:AccountingCustomerParty").find("cac:Party").find("cac:PartyIdentification").find("cbc:ID").text
    nombre_cliente = soup.find("cac:AccountingCustomerParty").find("cac:Party").find("cac:PartyLegalEntity").find("cbc:RegistrationName").text
    igv = soup.find("cac:TaxTotal").find("cbc:TaxAmount").text
    valor_venta = soup.find("cac:LegalMonetaryTotal").find("cbc:LineExtensionAmount").text
    total = soup.find("cbc:TaxInclusiveAmount").text

    row = [id, fecha, id_doc_ref, description, dni_ruc, nombre_cliente, valor_venta, igv, total]
    return row

def get_matrix_nc():
    path = "C:/Users/abernabel/Desktop/raw"
    files = os.listdir(path)
    matrix = list()
    for file in files:
        path_file = os.path.join(path, file)
        matrix.append(get_nc(path_file))
    return matrix


if __name__ == "__main__":
    path= "C:/Users/abernabel/Desktop/raw/20600768043-07-B201-00000376.XML"
    get_nc(path)
    matrix = get_matrix_nc()
    matrix.insert(0, ["ID NOTA DE CREDITO", "FECHA DE EMISION", "COD. REFERENCIA","DNI/RUC", "CLIENTE", "GLOSA", "VALOR VENTA", "IGV", "TOTAL"])
    wb = Workbook()
    ws = wb.active
    ws.title = "NC"
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            ws.cell(row=1+i, column=j+1).value = matrix[i][j]
    wb.save("test.xlsx")
