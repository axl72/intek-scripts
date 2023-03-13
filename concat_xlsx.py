import masterpath
import argparse
import pandas as pd
import openpyxl


def concatenar(dirpath, hojas=False):
    lista_directorios = masterpath.get_listdir(dirpath)
    if not hojas:
        lista_df = [pd.read_excel(path) for path in lista_directorios]
        df = pd.concat(lista_df)
        df.to_excel("concatenado.xlsx", index=False)
        return True
    elif hojas:
        lista_df = []
        for dir in lista_directorios:
            xl = pd.ExcelFile(dir)
            num_hojas = len(xl.sheet_names)
            for i in range(num_hojas):
                df = pd.read_excel(dir, sheet_name=i)
                lista_df.append(df)
        df = pd.concat(lista_df)
        df.to_excel("concatenado.xlsx", index=False)
        return True

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directorio")
    parser.add_argument("--hojas", action="store_true")
    argumentos = parser.parse_args()
    result = concatenar(argumentos.directorio, argumentos.hojas)
    print("Archivo generado exitosamente" if result else "Error al crear el archivo")
