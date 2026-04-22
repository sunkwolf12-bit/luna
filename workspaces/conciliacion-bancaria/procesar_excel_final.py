import pandas as pd
import json

file_path = '/root/.openclaw/media/inbound/file_32---c59bacf4-b855-451f-99c1-def80b25da27.xlsx'

try:
    # Según la salida anterior, los encabezados reales están en la fila 3 (índice 3 en skip)
    df = pd.read_excel(file_path, skiprows=3)
    
    # Limpiar filas completamente vacías
    df = df.dropna(how='all')
    
    # Asegurarnos de que las columnas tengan los nombres correctos
    df.columns = ['FOLIO', 'COBERTURA', 'FECHA', 'N_PAGO', 'MONTO', 'ENTREGADO', 'METODO_PAGO']
    
    # Convertir MONTO y FOLIO a tipos adecuados
    df['MONTO'] = pd.to_numeric(df['MONTO'], errors='coerce')
    df['FOLIO'] = pd.to_numeric(df['FOLIO'], errors='coerce', downcast='integer')
    
    # Filtrar filas donde FOLIO o MONTO sean NaN (cabeceras o basura)
    df = df.dropna(subset=['FOLIO', 'MONTO'])
    
    # Convertir FECHA a string para JSON
    df['FECHA'] = df['FECHA'].astype(str)
    
    # Guardar a JSON para uso posterior
    datos_lista = df.to_dict(orient='records')
    with open('/root/.openclaw/workspace/datos_sistema.json', 'w') as f:
        json.dump(datos_lista, f, indent=2)
    
    total = df['MONTO'].sum()
    conteo = len(df)
    
    print(f"Procesamiento exitoso.")
    print(f"Total de registros: {conteo}")
    print(f"Monto total sumado: ${total:,.2f}")
    
    # Mostrar una muestra para confirmar
    print("\nMuestra de datos procesados:")
    print(df.head(10).to_string())

except Exception as e:
    print(f"Error: {e}")
