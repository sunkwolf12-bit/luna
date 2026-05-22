---
name: excel-to-polished-pdf
description: Convert Excel workbooks, worksheets, CSV-style tables, or spreadsheet-based school/business activities into polished, presentation-ready PDF reports. Use when the user asks to generate, format, redesign, export, beautify, or arrange Excel information as a PDF, especially when the result should look professional rather than like a raw spreadsheet printout.
---

# Excel To Polished PDF

## Goal

Turn spreadsheet content into a designed PDF report. Preserve the workbook's meaning, calculations, section order, and important notes, while improving hierarchy, spacing, typography, table readability, and page flow.

Use the bundled script as a strong starting point:

```bash
python scripts/excel_to_polished_pdf.py --input "<workbook.xlsx>" --output "<report.pdf>"
```

Patch or replace the script when the workbook needs custom logic. The final PDF matters more than strict script reuse.

## Workflow

1. Inspect the workbook before designing.
   - Load workbook metadata, sheet names, used ranges, merged cells, images, formulas, cached values, and sample rows.
   - Identify titles, repeated table headers, blank bands, side-note columns, formulas, interpretations, totals, and summary rows.
   - Prefer cached/evaluated values for report tables. Preserve formula explanations as text when present.

2. Choose a report structure from the content.
   - Use a cover page when the workbook has a title, student/client name, date, multiple exercises, or multiple sheets.
   - Use one section per exercise/project/sheet/table group.
   - Put wide tables on landscape pages.
   - Use continuation pages with repeated section headers when notes or tables overflow.
   - Do not force everything onto one page if it becomes cramped.

3. Redesign the spreadsheet into document layout.
   - Use clear hierarchy: cover, section title, table, formula/key assumptions box, interpretation/notes box.
   - Use compact formats for large currency values (`$25.6M`, `$7.2K`) when it improves fit.
   - Keep source labels intact, but fix obvious encoding artifacts and whitespace.
   - Highlight important financial rows such as utilidad, EBIT, UAI/UAII, total, net income, result, balance, or status.
   - Repeat headers on continuation pages and never leave a continuation page without context.

4. Style with restraint.
   - Use a professional font available on the machine, such as Calibri or Arial on Windows.
   - Prefer landscape Letter/A4 for tables with many columns.
   - Use a sober palette: dark ink/navy for headers, one accent color, pale fills for note boxes, thin grid lines.
   - Avoid one-note palettes, heavy gradients, decorative blobs, and raw spreadsheet grid aesthetics.
   - Keep table text legible; split pages before shrinking below readable size.

5. Build the PDF.
   - Use bundled workspace runtimes when available.
   - Generate into a writable output folder unless the user requested another location.
   - If writing outside the workspace is required, request approval.
   - For simple workbooks, run `scripts/excel_to_polished_pdf.py`.
   - For unusual workbooks, copy the script into a scratch/workspace path and adapt section detection or layout.

6. Verify before final response.
   - Confirm the PDF exists and has nonzero size.
   - Check page count and page dimensions.
   - Extract text with a PDF library and confirm expected sheet/section titles are present.
   - Render or visually preview pages when tools allow it.
   - If render tools are unavailable, do programmatic checks and say only if verification was limited.
   - Check for orphan pages, clipped-looking table dimensions, missing titles, missing notes, and excessive blank space.

## Quality Bar

The result should look like a report designed from the Excel data, not like a screenshot or default print export.

Required traits:
- Cover page or strong first-page title when the source has multiple sections.
- Meaningful section breaks.
- Clean tables with visible headers and readable values.
- Notes/formulas separated from numeric tables.
- Consistent footer/page numbering.
- Output link to the final PDF.

Avoid:
- Raw Excel screenshots.
- Tiny unreadable printouts.
- Losing formulas, interpretations, or footnotes.
- Silent omission of sheets or sections.
- Pages that continue a table or notes without a section heading.

## References

Read `references/report-design-checklist.md` when designing or reviewing a PDF, especially for multi-page or visually important reports.
