import json

def comparar():
    with open('/root/.openclaw/workspace/datos_sistema.json', 'r') as f:
        sistema = json.load(f)
    
    with open('/root/.openclaw/workspace/datos_edgar.json', 'r') as f:
        edgar = json.load(f)

    # Agrupar sistema por folio para búsqueda rápida
    sistema_dict = {}
    for r in sistema:
        f = int(r['FOLIO'])
        if f not in sistema_dict:
            sistema_dict[f] = []
        sistema_dict[f].append(r)

    # Agrupar edgar por folio
    edgar_dict = {}
    for r in edgar:
        f = int(r['FOLIO'])
        if f not in edgar_dict:
            edgar_dict[f] = []
        edgar_dict[f].append(r)

    reporte = {
        "no_en_sistema": [],
        "diferencia_monto": [],
        "no_en_edgar": [],
        "totales": {
            "sistema": sum(r['MONTO'] for r in sistema),
            "edgar": sum(r['MONTO'] for r in edgar)
        }
    }

    # 1. Buscar lo que Edgar tiene que no está en sistema
    folios_vistos_sistema = set()
    for folio, registros in edgar_dict.items():
        if folio not in sistema_dict:
            for r in registros:
                reporte["no_en_sistema"].append(r)
        else:
            # Si el folio está, comparar montos
            # Tomamos el primero para simplificar, a menos que haya duplicados
            s_registros = sistema_dict[folio]
            for i, r_edgar in enumerate(registros):
                if i < len(s_registros):
                    r_sistema = s_registros[i]
                    if abs(r_edgar['MONTO'] - r_sistema['MONTO']) > 0.01:
                        reporte["diferencia_monto"].append({
                            "FOLIO": folio,
                            "FECHA": r_edgar['FECHA'],
                            "EDGAR": r_edgar['MONTO'],
                            "SISTEMA": r_sistema['MONTO'],
                            "DIF": r_edgar['MONTO'] - r_sistema['MONTO']
                        })
                else:
                    # Edgar tiene más registros de este folio que el sistema
                    reporte["no_en_sistema"].append(r_edgar)

    # 2. Buscar lo que el sistema tiene que Edgar no reportó
    for folio, registros in sistema_dict.items():
        if folio not in edgar_dict:
            for r in registros:
                reporte["no_en_edgar"].append(r)
        elif len(registros) > len(edgar_dict[folio]):
            # Sistema tiene más registros de este folio
            for i in range(len(edgar_dict[folio]), len(registros)):
                reporte["no_en_edgar"].append(registros[i])

    print(json.dumps(reporte, indent=2))

if __name__ == "__main__":
    comparar()
