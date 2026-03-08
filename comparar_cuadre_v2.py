import json

def comparar():
    with open('/root/.openclaw/workspace/datos_sistema.json', 'r') as f:
        sistema = json.load(f)
    
    with open('/root/.openclaw/workspace/datos_edgar.json', 'r') as f:
        edgar = json.load(f)

    # Agrupar sistema por folio
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
    for folio, registros in edgar_dict.items():
        if folio not in sistema_dict:
            for r in registros:
                # Omitir endosos de 125 si es necesario, pero aquí los mostramos
                reporte["no_en_sistema"].append(r)
        else:
            s_registros = sistema_dict[folio]
            for i, r_edgar in enumerate(registros):
                if i < len(s_registros):
                    r_sistema = s_registros[i]
                    # Solo reportar diferencias significativas (ignorando endosos que se pagan aparte)
                    if abs(r_edgar['MONTO'] - r_sistema['MONTO']) > 0.05:
                        reporte["diferencia_monto"].append({
                            "FOLIO": folio,
                            "FECHA": r_edgar['FECHA'],
                            "EDGAR": r_edgar['MONTO'],
                            "SISTEMA": r_sistema['MONTO'],
                            "DIF": r_edgar['MONTO'] - r_sistema['MONTO']
                        })
                else:
                    reporte["no_en_sistema"].append(r_edgar)

    # 2. Buscar lo que el sistema tiene que Edgar no reportó (o no vimos en fotos)
    for folio, registros in sistema_dict.items():
        if folio not in edgar_dict:
            for r in registros:
                # Solo nos interesan los cobros reales (no endosos) para el descuadre de efectivo
                if r['MONTO'] != 125:
                    reporte["no_en_edgar"].append(r)
        elif len(registros) > len(edgar_dict[folio]):
            for i in range(len(edgar_dict[folio]), len(registros)):
                if registros[i]['MONTO'] != 125:
                    reporte["no_en_edgar"].append(registros[i])

    print(json.dumps(reporte, indent=2))

if __name__ == "__main__":
    comparar()
