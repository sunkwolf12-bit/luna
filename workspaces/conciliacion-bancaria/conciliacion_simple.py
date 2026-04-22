import zipfile
import xml.etree.ElementTree as ET
import re

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
    except Exception as e:
        print(f"Error leyendo {filename}: {e}")
        return []

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
    rs_idx = cols.index('Razón Social') if 'Razón Social' in cols else -1
    for r in raw_contpaq[h_idx+1:]:
        if len(r) > max(f_idx, t_idx):
            folio = str(r[f_idx]).strip()
            if folio:
                try:
                    total = float(r[t_idx])
                    rs = r[rs_idx] if rs_idx != -1 else "N/A"
                    facturas[folio] = {'total': total, 'cliente': rs, 'cobrado': 0.0, 'origen': []}
                except: continue

# 2. EFECTIVO
pagos = []
for s in ['DEPOSITO1', 'DEPOSITO2', 'DEPOSITO3']:
    raw = read_xlsx_basic('/root/.openclaw/media/inbound/file_8---3c00f4a2-5481-48eb-a944-86ffe0f7be43.xlsx', sheet_name=s)
    h_idx = -1
    for i, r in enumerate(raw):
        if 'FACTURA' in r:
            h_idx = i
            cols = r
            break
    if h_idx != -1:
        f_idx = cols.index('FACTURA')
        m_idx = cols.index('MONTO')
        for r in raw[h_idx+1:]:
            if len(r) > max(f_idx, m_idx):
                folio = str(r[f_idx]).strip()
                if folio:
                    try:
                        monto = float(r[m_idx])
                        pagos.append({'folio': folio, 'monto': monto, 'origen': f'Efectivo-{s}'})
                    except: continue

# 3. BANCOS
raw_bancos = read_xlsx_basic('/root/.openclaw/media/inbound/file_9---ad70ca0b-fd9c-4173-a95e-eaa69129588e', sheet_name='FEBRERO')
h_idx = -1
for i, r in enumerate(raw_bancos):
    if '# FACTURA' in r:
        h_idx = i
        cols = r
        break
if h_idx != -1:
    f_idx = cols.index('# FACTURA')
    d_idx = cols.index('DEPOSITOS')
    c_idx = cols.index('CONCEPTO') if 'CONCEPTO' in cols else -1
    for r in raw_bancos[h_idx+1:]:
        if len(r) > max(f_idx, d_idx):
            concepto = str(r[c_idx]) if c_idx != -1 else ""
            if "VTA. FONDOS DE INV." in concepto: continue
            
            f_raw = str(r[f_idx]).strip()
            try:
                monto_total = float(r[d_idx])
                if f_raw and monto_total > 0:
                    folios = re.split(r'[/|Y|,|\s]+', f_raw)
                    folios = [f.strip() for f in folios if f.strip().isdigit()]
                    if folios:
                        m_ind = monto_total / len(folios)
                        for f in folios:
                            pagos.append({'folio': f, 'monto': m_ind, 'origen': 'Bancos'})
            except: continue

# 4. CRUCE
conciliadas = []
diferencias = []
pendientes = []
pagos_huerfanos = []

pagos_por_folio = {}
for p in pagos:
    f = p['folio']
    if f not in pagos_por_folio: pagos_por_folio[f] = []
    pagos_por_folio[f].append(p)

for folio, info in facturas.items():
    if folio in pagos_por_folio:
        monto_cobrado = sum(p['monto'] for p in pagos_por_folio[folio])
        info['cobrado'] = monto_cobrado
        info['origen'] = [p['origen'] for p in pagos_por_folio[folio]]
        if abs(info['total'] - monto_cobrado) < 1.0:
            conciliadas.append(folio)
        else:
            diferencias.append(folio)
    else:
        pendientes.append(folio)

for f in pagos_por_folio:
    if f not in facturas:
        pagos_huerfanos.append(f)

print(f"--- RESUMEN ---")
print(f"Facturas totales: {len(facturas)}")
print(f"Conciliadas: {len(conciliadas)}")
print(f"Con diferencia en monto: {len(diferencias)}")
print(f"Pendientes de cobro: {len(pendientes)}")
print(f"Cobros sin factura en sistema: {len(pagos_huerfanos)}")

if diferencias:
    print(f"\n--- DETALLE DE DIFERENCIAS ---")
    for f in diferencias[:10]:
        inf = facturas[f]
        print(f"Folio {f}: Facturado ${inf['total']:.2f} | Cobrado ${inf['cobrado']:.2f} ({', '.join(inf['origen'])})")
    if len(diferencias) > 10: print("...")

if pendientes:
    print(f"\n--- MUESTRA DE PENDIENTES (SIN COBRO) ---")
    for f in pendientes[:10]:
        inf = facturas[f]
        print(f"Folio {f}: {inf['cliente']} | ${inf['total']:.2f}")

if pagos_huerfanos:
    print(f"\n--- MUESTRA DE COBROS SIN FACTURA ---")
    for f in pagos_huerfanos[:10]:
        p = pagos_por_folio[f][0]
        print(f"Folio {f}: ${p['monto']:.2f} en {p['origen']}")
