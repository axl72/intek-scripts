import subprocess
import sys
import re
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("facture")
parser.add_argument(
    "--explorer", help="Permite encontrar obtener el directorio donde está almacenado el archivo", action="store_true")

OK = '\033[92m'  # GREEN
WARNING = '\033[93m'  # YELLOW
FAIL = '\033[91m'  # RED
RESET = '\033[0m'  # RESET COLOR


def open_file(path, opcion=None):
    # print(parser.parse_args())
    if parser.parse_args().explorer:
        subprocess.Popen(f'explorer /select,"{path}"')
        return
    subprocess.Popen([path], shell=True)


def get_listdir(path, result=[]):
    list_dir = os.listdir(path)
    list_dir = [os.path.join(path, dir) for dir in list_dir]
    for dir in list_dir:
        if os.path.isdir(dir):
            get_listdir(os.path.join(path, dir), result)
        elif os.path.isfile(dir):
            result.append(os.path.join(path, dir))
    return result


def get_facture_path(db_path, facture: str):
    files = get_listdir(db_path)
    for file in files:
        if re.search(facture, file):
            print(f"{OK}Comprobante {facture} encontrado{RESET}")
            return os.path.join(db_path, file)
    raise FileNotFoundError


def process_facture(facture):
    facture_processed = facture[:4] + "-0" + facture[4:]
    return facture_processed


def open_facture(db_path, facture: str):
    try:
        path = get_facture_path(db_path, facture)
        open_file(path)
    except FileNotFoundError:
        entidad = "boleta" if facture[0] == "B" else "factura"
        print(f"{WARNING}La {entidad} no pudo ser encontrada{RESET}")
        # db_path = db_path = "G:\\1.USUARIOS\\FACTURACION\COMPROBANTES\\2022"
        # path = get_facture_path(db_path, facture)
        # open_file(path)


def process_argv(argumentos: list):

    if len(argumentos) == 1:
        print(
            f"{FAIL}Ingrese el numero del comprobante - ejemplo: F1010004344{RESET}")
        return
    return argumentos[1]


if __name__ == "__main__":
    argumento = parser.parse_args().facture
    db_path = "G:\\1.USUARIOS\\FACTURACION\COMPROBANTES"
    if argumento != None:
        open_facture(db_path, process_facture(argumento))
