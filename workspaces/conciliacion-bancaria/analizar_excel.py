import pandas as pd
import json

file_path = '/root/.openclaw/media/inbound/file_32---c59bacf4-b855-451f-99c1-def80b25da27.xlsx'

try:
    # Leer todas las pestañas para ver qué hay
    xls = pd.ExcelFile(file_path)
    print(f"Pestañas encontradas: {xls.sheet_names}")
    
    # Suponiendo que la información está en la primera pestaña
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    
    # Mostrar las primeras filas y columnas para entender la estructura
    print("\nColumnas del archivo:")
    print(df.columns.tolist())
    
    print("\nPrimeras 5 filas:")
    print(df.head().to_string())

except Exception as e:
    print(f"Error al leer el archivo: {e}")
