import sys
import pandas as pd


def validar_formato(dataframe, formato_base: list[str]):
    columnas = dataframe.columns.values
    size = len(formato_base)
    for i in range(size):
        if formato_base[i] != columnas[i]:
            message = f"El campo {columnas[i]} no coincide con {formato_base[i]}"
            raise Exception(message)
    print("Formato valido")


def validar_codigos_origen(dataframe):
    if len(dataframe[dataframe["COD. ORIGEN"].isnull()].index):
        dataframe[dataframe["COD. ORIGEN"].isnull()].to_excel(
            "log-sku-isnull.xlsx", index=False)
        raise Exception("Las siguientes filas no tienen codigo de origen")
    print("Todas las filas tienen codigo de origen")
    df = dataframe.groupby(["COD. ORIGEN"], as_index=False).size()
    if len(df[df['size'] != 1].index) > 0:
        df[df['size'] != 1].to_excel("log-duplicated.sku.xlsx", index=False)
        raise Exception("Existen SKU repetidos")
    print("Validación de codigos de orige no repetidos exitosa")


def combinar_listas(dataframe1, dataframe2):
    nueva_lista_tmp = pd.concat([dataframe1, dataframe2])
    nueva_lista_tmp = nueva_lista_tmp.drop_duplicates(
        keep='last', subset=['COD. ORIGEN'])
    nueva_lista_tmp = nueva_lista_tmp.sort_values(
        "LINEA", ascending=False).reset_index()
    return nueva_lista_tmp


if __name__ == "__main__":
    filename_lista_base = sys.argv[1]
    filename_nuevos_precios = sys.argv[2]
    fecha_actualizacion = sys.argv[3]
    formato_base = ["COD. ORIGEN", "LINEA", "DESCRIPCION",
                    "MASTER PACK", "PVP", "MARGEN 30%", "FECHA DE ACTUALIZACION"]

    formato_nueva_lista = ["COD. ORIGEN", "LINEA",
                           "DESCRIPCION", "MASTER PACK", "PVP"]

    base = pd.read_excel(filename_lista_base, index_col=None)
    validar_formato(base, formato_base)
    validar_codigos_origen(base)
    nueva_lista = pd.read_excel(filename_nuevos_precios)
    validar_formato(nueva_lista, formato_nueva_lista)
    validar_codigos_origen(nueva_lista)
    nueva_lista["MARGEN 30%"] = nueva_lista["PVP"]*0.7
    nueva_lista["FECHA DE ACTUALIZACION"] = fecha_actualizacion
    result = combinar_listas(base, nueva_lista)
    fecha_formateada = fecha_actualizacion.replace("/", "")
    nombre_export = f'LP-{fecha_formateada}.xlsx'
    print(nombre_export)
    result = result.drop("index", axis=1)
    result.to_excel(nombre_export, sheet_name=fecha_actualizacion.replace(
        "/", "."), index=False)
