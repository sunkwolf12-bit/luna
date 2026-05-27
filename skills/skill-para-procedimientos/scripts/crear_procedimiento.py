#!/usr/bin/env python3
"""
Crea un procedimiento institucional a partir del archivo base y un Word fuente.
Uso: python3 crear_procedimiento.py <archivo_fuente.docx> <CLAVE> <NOMBRE> <FECHA> [DEPARTAMENTO]

Ejemplo:
  python3 crear_procedimiento.py PCD1_seguimiento.docx PCD1 "PROCEDIMIENTO DE SEGUIMIENTO A COBRANZA ATRASADA" "25/10/2025" "Cobranza"

Salida: workspaces/instructivos/CLAVE_NOMBRE_SANITIZADO.docx
"""
import sys, os, re, shutil, zipfile, unicodedata
from docx import Document
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

WORKSPACE = '/home/elena/.openclaw/workspace'
BASE_FILE = os.path.join(WORKSPACE, 'workspaces/instructivos/FORMATO_INSTITUCIONAL_PROCEDIMIENTO_2025.docx')
OUT_DIR = os.path.join(WORKSPACE, 'workspaces/instructivos')

def slug(text):
    """Convierte texto a un nombre de archivo seguro (sin acentos, mayusculas, solo A-Z0-9_)"""
    s = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^A-Z0-9]+', '_', s.upper()).strip('_')

def insert_paragraph_after(paragraph, text):
    """Inserta un nuevo parrafo con 'text' justo despues de 'paragraph'."""
    new_p = OxmlElement('w:p')
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    new_para.add_run(text)
    return new_para

def patch_header(docx_path, nombre, fecha, clave, departamento):
    """Modifica header2.xml y document.xml directamente en el ZIP."""
    with zipfile.ZipFile(docx_path, 'r') as z:
        files = {n: z.read(n) for n in z.namelist()}

    # --- DOCUMENT.XML: portada ---
    files['word/document.xml'] = files['word/document.xml'].replace(
        b'PROCEDIMIENTO EN BLANCO', nombre.encode('utf-8'))

    # --- HEADER2.XML ---
    h2 = files.get('word/header2.xml') or files.get('word/header1.xml', b'')
    if not h2:
        print("ERROR: No se encontro header2.xml ni header1.xml en el archivo base")
        return

    # 1) Titulo en encabezado
    h2 = h2.replace(b'PROCEDIMIENTO EN BLANCO', nombre.encode('utf-8'))

    # 2) Fecha - patron original: 31/08/202</w:t></w:r><w:r w:rsidR="00BF75E2"><w:t>5</w:t>
    h2 = h2.replace(b'31/08/202</w:t></w:r><w:r w:rsidR="00BF75E2"><w:t>5</w:t>',
                    (fecha + '</w:t>').encode())

    # 3) CLAVE - insertar en parrafo vacio de la fila siguiente a CLAVE:
    clave_pos = h2.find(b'CLAVE:')
    next_tr = h2.find(b'<w:tr ', clave_pos)
    row_end = h2.find(b'</w:tr>', next_tr)
    clave_para_end = h2.find(b'</w:pPr></w:p>', next_tr)
    if clave_para_end > 0 and clave_para_end < row_end:
        insert = ('</w:pPr><w:r><w:rPr><w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t>'
                  + clave + '</w:t></w:r></w:p>').encode()
        h2 = h2[:clave_para_end] + insert + h2[clave_para_end + len(b'</w:pPr></w:p>'):]

    # 4) DEPARTAMENTO - insertar en parrafo vacio justo despues de DEPARTAMENTO:
    dep_pos = h2.find(b'DEPARTAMENTO:')
    ppr = h2.find(b'<w:pPr>', dep_pos + 100)
    ppr_end = h2.find(b'</w:pPr>', ppr)
    para_end = h2.find(b'</w:p>', ppr_end)
    if ppr > 0 and para_end > ppr:
        between = h2[ppr_end + len(b'</w:pPr>'):para_end]
        if between.strip() == b'':
            insert2 = ('<w:r><w:rPr><w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t>'
                       + departamento + '</w:t></w:r>').encode()
            h2 = h2[:para_end] + insert2 + h2[para_end:]

    files['word/header2.xml'] = h2

    # Escribir ZIP final
    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)

def fill_body(docx_path, objetivo, alcance, docref_lines, def_lines, des_lines):
    """Rellena las secciones del cuerpo del documento."""
    d = Document(docx_path)
    labels = ['OBJETIVO:', 'ALCANCE:', 'DOCUMENTOS DE REFERENCIA:', 'DEFINICIONES:', 'DESARROLLO']

    # Eliminar contenido existente entre etiquetas
    for label_name in reversed(labels):
        cur_i = None
        for j, pp in enumerate(d.paragraphs):
            if pp.text.strip().upper() == label_name:
                cur_i = j
                break
        if cur_i is None:
            continue
        nxt = None
        for j in range(cur_i + 1, len(d.paragraphs)):
            if d.paragraphs[j].text.strip().upper() in labels:
                nxt = j
                break
        if nxt is None:
            nxt = len(d.paragraphs)
        for _ in range(nxt - cur_i - 1):
            rm = d.paragraphs[cur_i + 1]
            rm._element.getparent().remove(rm._element)

    def find(label):
        for p in d.paragraphs:
            if p.text.strip().upper() == label:
                return p
        raise ValueError(f'Label no encontrado: {label}')

    cur = find('OBJETIVO:')
    insert_paragraph_after(cur, objetivo)
    cur = find('ALCANCE:')
    insert_paragraph_after(cur, alcance)
    cur = find('DOCUMENTOS DE REFERENCIA:')
    last = cur
    for line in docref_lines:
        last = insert_paragraph_after(last, line)
    cur = find('DEFINICIONES:')
    last = cur
    for line in def_lines:
        last = insert_paragraph_after(last, line)
    cur = find('DESARROLLO')
    last = cur
    for line in des_lines:
        last = insert_paragraph_after(last, line)

    d.save(docx_path)


def main():
    if len(sys.argv) < 5:
        print("Uso: python3 crear_procedimiento.py <fuente.docx> <CLAVE> <NOMBRE> <FECHA> [DEPARTAMENTO]")
        sys.exit(1)

    fuente = sys.argv[1]
    clave = sys.argv[2].strip()
    nombre = sys.argv[3].strip()
    fecha = sys.argv[4].strip()
    departamento = sys.argv[5].strip() if len(sys.argv) > 5 else 'Cobranza'

    if not os.path.exists(fuente):
        print(f"ERROR: Archivo fuente no encontrado: {fuente}")
        sys.exit(1)
    if not os.path.exists(BASE_FILE):
        print(f"ERROR: Archivo base no encontrado: {BASE_FILE}")
        sys.exit(1)

    out_name = f"{clave}_{slug(nombre)}.docx"
    out_path = os.path.join(OUT_DIR, out_name)

    # --- PASO 1: Extraer contenido del archivo fuente ---
    src = Document(fuente)
    sp = [p.text.rstrip() for p in src.paragraphs if p.text.strip()]

    def idx(pattern):
        for i, t in enumerate(sp):
            if re.match(pattern, t.strip(), re.I):
                return i
        return None

    i_obj = idx(r'^1\.?\s*OBJETIVO')
    i_alc = idx(r'^2\.?\s*ALCANCE')
    i_resp = idx(r'^3\.?\s*RESPONSABLES')

    objetivo = sp[i_obj + 1] if i_obj is not None and i_obj + 1 < len(sp) else ''
    alcance = sp[i_alc + 1] if i_alc is not None and i_alc + 1 < len(sp) else ''
    start = i_resp if i_resp is not None else 0
    des_lines = sp[start:]

    # Generar DOCUMENTOS DE REFERENCIA si no existen en fuente
    docref_generados = [
        'CRM PROTEG-RT y/o SIGA (segun aplique al procedimiento).',
        'Archivos internos de respaldo mencionados en el procedimiento.'
    ]
    # Ver si la fuente menciona docs especificos
    for line in sp:
        up = line.upper()
        if 'CRM' in up:
            docref_generados[0] = f'CRM PROTEG-RT (mencionado en el procedimiento).'
        if 'SIGA' in up:
            docref_generados[0] = 'SIGA y CRM PROTEG-RT (mencionados en el procedimiento).'
        if 'PAGOS_V' in up or 'PAGOS V' in up:
            docref_generados[1] = 'Archivo Pagos_V3 (segun referencia en el procedimiento).'

    defs_generados = [
        'Definiciones basadas en el contenido del procedimiento.',
    ]
    # Extraer definiciones del texto si hay patrones
    for line in sp:
        if ':' in line and len(line.split(':')[0].split()) <= 5:
            # Podria ser una definicion tipo "X: es..."
            pass

    # --- PASO 2: Copiar base y parchar ---
    shutil.copyfile(BASE_FILE, out_path)
    patch_header(out_path, nombre, fecha, clave, departamento)
    fill_body(out_path, objetivo, alcance, docref_generados, defs_generados, des_lines)

    print(f"Procedimiento creado: {out_path}")
    print(f"  CLAVE: {clave}")
    print(f"  NOMBRE: {nombre}")
    print(f"  FECHA: {fecha}")
    print(f"  DEPARTAMENTO: {departamento}")

if __name__ == '__main__':
    main()
