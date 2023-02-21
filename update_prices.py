import openpyxl
import sys
import pandas as pd
from datetime import date
import os

def update_date_df(dataframe, curret_date:str=date.today()) -> str:
    datevar = curret_date
    dataframe['Fecha de actualizacion'] = datevar
    return datevar.__str__().replace('-', '.')

def create_base_prices_list(path_file:str, margin:int=0.3):
    """La lista de de precios inicial debe tener los siguientes campos: 'Codigo de origen', 'Descripcion Producto', 'Master Pack', 'PVP'.
    El margen por defectdo es 30%, lo cual significa que la lista de precios base se generará en base a ese margen base."""
    df = pd.read_excel(path_file)
    df['30%'] = df['PVP']*(1-margin)
    datestr = update_date_df(df, '11-11-2022')
    df.to_excel('result.xlsx', index=False, sheet_name=datestr)
  #  os.system("result.xlsx")

def update_prices(base_list_prices_path:str, new_list_prices_path:str):
    df_base = pd.read_excel(base_list_prices_path)
    new_df = pd.read_excel(new_list_prices_path)
    new_df['30%'] = new_df['PVP']*0.3
    datastr=update_date_df(new_df, '01-02-2023')
    updated_prices_list = pd.concat([df_base, new_df], ignore_index=True, axis=0).drop_duplicates(keep='last', subset=['COD. ORIGEN'])
    updated_prices_list.to_excel('result.xlsx', index=False, sheet_name=datastr)

if __name__ == "__main__":
    try:
        prices_lists_path = sys.argv[1]
        print(f"La lista de precios base es: {prices_lists_path}")
        new_prices_path = sys.argv[2]
        print(f"La lista de nuevos precios es: {new_prices_path}")
        create_base_prices_list(prices_lists_path)
        update_prices('result.xlsx', new_prices_path)
        print("Prices List Update Successfully")
        os.system('result.xlsx')
    except PermissionError:
        print(f"El archivo result.xlsx no puede ser accedido")


