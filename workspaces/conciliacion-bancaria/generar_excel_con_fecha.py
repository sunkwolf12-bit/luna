import zipfile
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timedelta

def excel_date_to_str(serial):
    try:
        # Excel dates are days since Dec 30, 1899
        dt = datetime(1899, 12, 30) + timedelta(days=float(serial))
        return dt.strftime('%d/%m/%Y')
    except:
        return str(serial)

def read_xlsx_basic(filename, sheet_name=None, sheet_index=1):
    ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    try:
        with zipfile.ZipFile(filename, 'r') as z:
            with z.open('xl/sharedStrings.xml') as f:
                strings = [node.text if node.text else "" for node in ET.parse(f).findall('.//ns:t', ns)]
            if sheet_name:
                with z.open('xl/workbook.xml') as f:
                    tree = ET.parse(f)
                    for i, node in enumerate(tree.findall('.//ns:sheet', ns), 1):
                        if node.get('name').upper() == sheet_name.upper():
                            sheet_index = i
                            break
            data = []
            with z.open(f'xl/worksheets/sheet{sheet_index}.xml') as f:
                root = ET.parse(f).getroot()
                for row in root.findall('.//ns:row', ns):
                    vals = []
                    for c in row.findall('ns:c', ns):
                        v = c.find('ns:v', ns)
                        val = ""
                        if v is not None:
                            t = c.get('t')
                            val = v.text
                            if t == 's': val = strings[int(val)]
                        vals.append(val)
                    data.append(vals)
            return data
    except: return []

# 1. CONTPAQ
raw_contpaq = read_xlsx_basic('/root/.openclaw/media/inbound/file_7---dfabd2d8-a203-4361-bc46-bf15bdcab5ad.xlsx')
facturas = {}
h_idx = -1
for i, row in enumerate(raw_contpaq):
    if 'Folio' in row and 'Total' in row:
        h_idx = i
        cols = row
        break

if h_idx != -1:
    f_idx = cols.index('Folio')
    t_idx = cols.index('Total')
    d_idx = cols.index('Fecha') if 'Fecha' in cols else -1
    rs_idx = cols.index('Razón Social') if 'Razón Social' in cols else -1
    for r in raw_contpaq[h_idx+1:]:
        if len(r) > max(f_idx, t_idx):
            folio = str(r[f_idx]).strip()
            if folio:
                try:
                    total = float(r[t_idx])
                    fecha_raw = r[d_idx] if d_idx != -1 else "N/A"
                    # Si la fecha es un número de Excel, convertirla
                    if fecha_raw.replace('.','',1).isdigit():
                        fecha = excel_date_to_str(fecha_raw)
                    else:
                        fecha = fecha_raw
                    facturas[folio] = {
                        'total': total, 
                        'cliente': r[rs_idx] if rs_idx != -1 else "N/A",
                        'fecha': fecha
                    }
                except: continue

# 2. Recopilar todos los folios pagados (Efectivo 1, 2, 3 y Bancos)
pagos_folios = set()
for s in ['DEPOSITO1', 'DEPOSITO2', 'DEPOSITO3']:
    raw = read_xlsx_basic('/root/.openclaw/media/inbound/file_8---3c00f4a2-5481-48eb-a944-86ffe0f7be43.xlsx', sheet_name=s)
    h_idx = -1
    for i, r in enumerate(raw):
        if 'FACTURA' in r: h_idx = i; cols = r; break
    if h_idx != -1:
        f_idx = cols.index('FACTURA')
        for r in raw[h_idx+1:]:
            if len(r) > f_idx:
                folio = str(r[f_idx]).strip()
                if folio: pagos_folios.add(folio)

raw_bancos = read_xlsx_basic('/root/.openclaw/media/inbound/file_9---ad70ca0b-fd9c-4173-a95e-eaa69129588e', sheet_name='FEBRERO')
h_idx = -1
for i, r in enumerate(raw_bancos):
    if '# FACTURA' in r: h_idx = i; cols = r; break
if h_idx != -1:
    f_idx = cols.index('# FACTURA')
    for r in raw_bancos[h_idx+1:]:
        if len(r) > f_idx:
            f_raw = str(r[f_idx]).strip()
            if f_raw:
                folios = re.split(r'[/|Y|,|\s]+', f_raw)
                for f in folios:
                    f_clean = f.strip()
                    if f_clean.isdigit(): pagos_folios.add(f_clean)

# Generar CSV final con FECHA
with open('Facturas_Pendientes_Con_Fecha.csv', 'w', encoding='utf-16') as f:
    f.write("Fecha\tFolio\tCliente\tMonto\n")
    for folio, info in facturas.items():
        if folio not in pagos_folios:
            f.write(f"{info['fecha']}\t{folio}\t{info['cliente']}\t{info['total']}\n")

print("CSV Generado con éxito.")
