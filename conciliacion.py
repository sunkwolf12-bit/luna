import pandas as pd
import zipfile
import xml.etree.ElementTree as ET
import re

def read_xlsx_basic(filename, sheet_name=None, sheet_index=1):
    ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(filename, 'r') as z:
        # Load strings
        with z.open('xl/sharedStrings.xml') as f:
            strings = [node.text for node in ET.parse(f).findall('.//ns:t', ns)]
        
        # Determine sheet file
        if sheet_name:
            with z.open('xl/workbook.xml') as f:
                tree = ET.parse(f)
                for i, node in enumerate(tree.findall('.//ns:sheet', ns), 1):
                    if node.get('name').upper() == sheet_name.upper():
                        sheet_index = i
                        break
        
        # Read sheet
        data = []
        with z.open(f'xl/worksheets/sheet{sheet_index}.xml') as f:
            root = ET.parse(f).getroot()
            for row in root.findall('.//ns:row', ns):
                vals = []
                for c in row.findall('ns:c', ns):
                    v = c.find('ns:v', ns)
                    val = None
                    if v is not None:
                        t = c.get('t')
                        val = v.text
                        if t == 's': val = strings[int(val)]
                    vals.append(val)
                data.append(vals)
        return data

# 1. Procesar CONTPAQ
print("Procesando CONTPAQ...")
raw_contpaq = read_xlsx_basic('/root/.openclaw/media/inbound/file_7---dfabd2d8-a203-4361-bc46-bf15bdcab5ad.xlsx')
# Buscar encabezado
header_idx = 0
for i, row in enumerate(raw_contpaq):
    if 'Folio' in row and 'Total' in row:
        header_idx = i
        break
df_contpaq = pd.DataFrame(raw_contpaq[header_idx+1:], columns=raw_contpaq[header_idx])
df_contpaq = df_contpaq.dropna(subset=['Folio', 'Total'])
df_contpaq['Folio'] = df_contpaq['Folio'].astype(str)
df_contpaq['Total'] = pd.to_numeric(df_contpaq['Total'], errors='coerce')

# 2. Procesar EFECTIVO (3 hojas)
print("Procesando EFECTIVO...")
pagos_efectivo = []
for s in ['DEPOSITO1', 'DEPOSITO2', 'DEPOSITO3']:
    raw = read_xlsx_basic('/root/.openclaw/media/inbound/file_8---3c00f4a2-5481-48eb-a944-86ffe0f7be43.xlsx', sheet_name=s)
    h_idx = 0
    for i, r in enumerate(raw):
        if 'FACTURA' in r:
            h_idx = i
            break
    cols = raw[h_idx]
    for r in raw[h_idx+1:]:
        if len(r) >= len(cols):
            d = dict(zip(cols, r))
            if d.get('FACTURA'):
                pagos_efectivo.append({
                    'Folio': str(d['FACTURA']),
                    'Monto': pd.to_numeric(d['MONTO'], errors='coerce'),
                    'Origen': f'Efectivo ({s})'
                })

# 3. Procesar BANCOS
print("Procesando BANCOS...")
raw_bancos = read_xlsx_basic('/root/.openclaw/media/inbound/file_9---ad70ca0b-fd9c-4173-a95e-eaa69129588e', sheet_name='FEBRERO')
h_idx = 0
for i, r in enumerate(raw_bancos):
    if '# FACTURA' in r:
        h_idx = i
        break
cols = raw_bancos[h_idx]
pagos_bancos = []
for r in raw_bancos[h_idx+1:]:
    if len(r) >= len(cols):
        d = dict(zip(cols, r))
        concepto = str(d.get('CONCEPTO', ''))
        if "VTA. FONDOS DE INV." in concepto:
            continue
        
        folios_raw = str(d.get('# FACTURA', ''))
        monto = pd.to_numeric(d.get('DEPOSITOS'), errors='coerce')
        
        if folios_raw and folios_raw != 'None' and monto > 0:
            # Separar folios como 47772/47773 o 47772 Y 47773
            folios = re.split(r'[/|Y|,|\s]+', folios_raw)
            folios = [f.strip() for f in folios if f.strip().isdigit()]
            
            if len(folios) > 0:
                monto_por_folio = monto / len(folios)
                for f in folios:
                    pagos_bancos.append({
                        'Folio': f,
                        'Monto': monto_por_folio,
                        'Origen': 'Bancos'
                    })

# 4. Conciliar
df_pagos = pd.DataFrame(pagos_efectivo + pagos_bancos)
df_resumen = df_contpaq.merge(df_pagos, left_on='Folio', right_on='Folio', how='outer', indicator=True)

conciliadas = df_resumen[df_resumen['_merge'] == 'both']
pendientes_cobro = df_resumen[df_resumen['_merge'] == 'left_only']
pagos_sin_factura = df_resumen[df_resumen['_merge'] == 'right_only']

print("\n--- RESULTADOS DE LA CONCILIACIÓN ---")
print(f"Total Facturas en CONTPAQ: {len(df_contpaq)}")
print(f"Facturas Conciliadas: {len(conciliadas)}")
print(f"Facturas Pendientes de Cobro: {len(pendientes_cobro)}")
print(f"Pagos sin Factura Identificada: {len(pagos_sin_factura)}")

# Verificar diferencias de monto en conciliadas
print("\n--- DIFERENCIAS DE MONTO ---")
diferencias = conciliadas[abs(conciliadas['Total'] - conciliadas['Monto']) > 1]
if len(diferencias) > 0:
    print(diferencias[['Folio', 'Total', 'Monto', 'Origen']])
else:
    print("No se encontraron diferencias significativas de monto en las facturas conciliadas.")

