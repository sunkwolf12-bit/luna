import zipfile, re

path = 'workspaces/instructivos/PAC3.docx'
with zipfile.ZipFile(path, 'r') as z:
    xml_map = {name: z.read(name) for name in z.namelist()}

doc_xml = xml_map['word/document.xml'].decode('utf-8', errors='replace')

# Add sectPr before </w:body>
sectPr = '<w:sectPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:headerReference w:type="even" r:id="rId9"/><w:headerReference w:type="default" r:id="rId10"/><w:footerReference w:type="default" r:id="rId11"/><w:headerReference w:type="first" r:id="rId12"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1417" w:right="1701" w:bottom="1417" w:left="1701" w:header="709" w:footer="397" w:gutter="0"/><w:cols w:space="708"/><w:titlePg/></w:sectPr>'

# Insert before </w:body>
doc_xml_new = doc_xml.replace('</w:body>', sectPr + '</w:body>')

# Verify
if '<w:sectPr' in doc_xml_new and '<w:headerReference' in doc_xml_new:
    print('✅ sectPr with headers added')
else:
    print('❌ Failed')

xml_map['word/document.xml'] = doc_xml_new.encode('utf-8')
with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in xml_map.items():
        zout.writestr(name, data)
print('✅ Saved')

# Verify by checking header2 texts
with zipfile.ZipFile(path, 'r') as z:
    h2 = z.read('word/header2.xml').decode('utf-8', errors='replace')
    texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', h2)
    print(f'Header2 texts: {texts}')

# Also check the document has the header references
with zipfile.ZipFile(path, 'r') as z:
    doc2 = z.read('word/document.xml').decode('utf-8', errors='replace')
    hdrs = re.findall(r'<w:headerReference[^>]*/>', doc2)
    print(f'Header refs in document: {hdrs}')