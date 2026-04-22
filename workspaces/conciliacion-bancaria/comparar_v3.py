import json

def comparar_v3():
    with open('/root/.openclaw/workspace/datos_sistema.json', 'r') as f:
        sistema = json.load(f)
    with open('/root/.openclaw/workspace/datos_edgar.json', 'r') as f:
        edgar = json.load(f)

    # Filtrar endosos de $125 (ya que se pagan aparte)
    sistema_cobros = [r for r in sistema if abs(r['MONTO'] - 125.0) > 0.01]
    edgar_cobros = [r for r in edgar if abs(r['MONTO'] - 125.0) > 0.01]
    
    endosos_sistema = [r for r in sistema if abs(r['MONTO'] - 125.0) < 0.01]
    endosos_edgar = [r for r in edgar if abs(r['MONTO'] - 125.0) < 0.01]

    # Diccionarios para búsqueda
    s_dict = {}
    for r in sistema_cobros:
        f = int(r['FOLIO'])
        if f not in s_dict: s_dict[f] = []
        s_dict[f].append(r)

    e_dict = {}
    for r in edgar_cobros:
        f = int(r['FOLIO'])
        if f not in e_dict: e_dict[f] = []
        e_dict[f].append(r)

    reporte = {
        "no_en_sistema": [],
        "diferencia_monto": [],
        "no_en_edgar": [],
        "endosos": {
            "en_sistema": [r['FOLIO'] for r in endosos_sistema],
            "en_edgar": [r['FOLIO'] for r in endosos_edgar]
        },
        "totales": {
            "cobros_sistema": sum(r['MONTO'] for r in sistema_cobros),
            "cobros_edgar": sum(r['MONTO'] for r in edgar_cobros)
        }
    }

    # 1. Edgar vs Sistema
    for folio, registros in e_dict.items():
        if folio not in s_dict:
            for r in registros: reporte["no_en_sistema"].append(r)
        else:
            s_regs = s_dict[folio]
            for i, r_e in enumerate(registros):
                if i < len(s_regs):
                    r_s = s_regs[i]
                    if abs(r_e['MONTO'] - r_s['MONTO']) > 0.1:
                        reporte["diferencia_monto"].append({
                            "FOLIO": folio, "FECHA": r_e['FECHA'],
                            "EDGAR": r_e['MONTO'], "SISTEMA": r_s['MONTO'],
                            "DIF": r_e['MONTO'] - r_s['MONTO']
                        })
                else:
                    reporte["no_en_sistema"].append(r_e)

    # 2. Sistema vs Edgar
    for folio, registros in s_dict.items():
        if folio not in e_dict:
            for r in registros: reporte["no_en_edgar"].append(r)
        elif len(registros) > len(e_dict[folio]):
            for i in range(len(e_dict[folio]), len(registros)):
                reporte["no_en_edgar"].append(registros[i])

    print(json.dumps(reporte, indent=2))

if __name__ == "__main__":
    comparar_v3()
