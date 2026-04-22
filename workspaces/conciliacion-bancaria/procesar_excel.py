import pandas as pd

file_path = '/root/.openclaw/media/inbound/file_32---c59bacf4-b855-451f-99c1-def80b25da27.xlsx'

try:
    # Leer el archivo saltando las filas vacías iniciales
    # Según la salida anterior, los encabezados reales están en la fila 2 (índice 2)
    df = pd.read_excel(file_path, skiprows=2)
    
    # Limpiar filas completamente vacías
    df = df.dropna(how='all')
    
    # Resetear el índice
    df = df.reset_index(drop=True)
    
    print("Columnas detectadas:")
    print(df.columns.tolist())
    
    print("\nPrimeras 10 filas de datos:")
    print(df.head(10).to_string())
    
    # Guardar en un JSON temporal para que Luna pueda leerlo más fácil si es necesario
    df.to_json('/root/.openclaw/workspace/datos_sistema.json', orient='records', indent=2)
    
    # Calcular el total del sistema para comparar con la imagen
    if 'MONTO' in df.columns:
        # Asegurarse que MONTO sea numérico
        df['MONTO'] = pd.to_numeric(df['MONTO'], errors='coerce')
        total = df['MONTO'].sum()
        print(f"\nTotal calculado en Excel: ${total:,.2f}")

except Exception as e:
    print(f"Error procesando el Excel: {e}")
