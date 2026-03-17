from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
import datetime
from typing import List
from ..compatibility_analyzer import CompatibilityIssue

# Helper for OXML
# --- OXML Helpers (Safe Insertion) ---
def get_or_add_child(parent, tag_name, order_list=None):
    if order_list is None:
        order_list = []
    child = parent.find(qn(tag_name))
    if child is not None:
        return child
    child = OxmlElement(tag_name)
    
    if order_list:
        try:
            my_idx = order_list.index(tag_name)
            for i in range(my_idx + 1, len(order_list)):
                next_tag = order_list[i]
                next_element = parent.find(qn(next_tag))
                if next_element is not None:
                    parent.insert(parent.index(next_element), child)
                    return child
        except ValueError:
            pass
            
    parent.append(child)
    return child

TBL_PR_ORDER = ['w:tblStyle', 'w:tblpPr', 'w:tblOverlap', 'w:bidiVisual', 'w:tblStyleRowBandSize', 'w:tblStyleColBandSize', 'w:tblW', 'w:jc', 'w:tblCellSpacing', 'w:tblInd', 'w:tblBorders', 'w:shd', 'w:tblLayout', 'w:tblCellMar', 'w:tblLook']
TC_PR_ORDER = ['w:cnfStyle', 'w:tcW', 'w:gridSpan', 'w:hMerge', 'w:vMerge', 'w:tcBorders', 'w:shd', 'w:noWrap', 'w:tcMar', 'w:textDirection', 'w:tcFitText', 'w:vAlign', 'w:hideMark', 'w:headers', 'w:cellIns', 'w:cellDel', 'w:cellMerge', 'w:tcPrChange']

class CompatibilityDocxGenerator:
    def _set_repeat_header(self, row):
        trPr = row._tr.get_or_add_trPr()
        tblHeader = get_or_add_child(trPr, 'w:tblHeader', [])
        return row

    """
    Generates a Word Document (.docx) detailing Interface Compatibility issues.
    """
    def __init__(self, issues: List[CompatibilityIssue], old_path: str, new_path: str, template_path: str = None, spec1: dict = None, spec2: dict = None):
        self.issues = issues
        self.old_path = old_path
        self.new_path = new_path
        self.spec1 = spec1 or {}
        self.spec2 = spec2 or {}
        
        if template_path and os.path.exists(template_path):
            self.doc = Document(template_path)
        else:
            # Fallback to resources directory
            res_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "resources", "diff_templates"))
            comp_temp = os.path.join(res_dir, "template_compatibility.docx")
            if os.path.exists(comp_temp):
                self.doc = Document(comp_temp)
            elif os.path.exists("template.docx"):
                self.doc = Document("template.docx")
            else:
                self.doc = Document()
            
        self._setup_styles()

    def _setup_styles(self):
        # Normal text
        normal = self.doc.styles['Normal']
        normal.font.name = 'Segoe UI'
        normal.font.size = Pt(10)

        # Title
        if 'Title' in self.doc.styles:
            style = self.doc.styles['Title']
            style.font.name = 'Georgia'
            style.font.size = Pt(22)
            style.font.bold = True
            style.font.color.rgb = RGBColor(31, 78, 121)

    def generate(self, output_path: str):
        """Builds the document structure and saves it."""
        self.doc.add_heading('OpenAPI Comparison - Interface Compatibility Report', 0)
        
        # 1. Metadata Table
        self._add_metadata_table()

        # 2. Executive Summary or Total Count

        
        if not self.issues:
             self.doc.add_paragraph("No interface compatibility discrepancies were found. The specifications are fully compatible in terms of request/response payloads and parameters.")
             self.doc.save(output_path)
             return

        # 3. List of Issues (Table grouped by Path/Method)

        # 4. Summary Section

        self.doc.add_heading('Summary', 1)
        
        freq = {}
        for issue in self.issues:
             key = (issue.issue_type, issue.details)
             freq[key] = freq.get(key, 0) + 1
        self.doc.add_paragraph().add_run(f'Total Issues Found: {len(self.issues)}').bold = True
             
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        widths_s = [Inches(0.4), Inches(2.2), Inches(3.4), Inches(1.0)] # total 7.0
        table = self._create_table(4, widths_s)
        hdr = table.rows[0].cells
        self._set_repeat_header(table.rows[0])
        hdr[0].text = '#'
        hdr[1].text = 'Issue Type'
        hdr[2].text = 'Details'
        hdr[3].text = 'Frequency'
        hdr[1].text = "Details"
        hdr[2].text = "Frequency"
        for t in hdr:
            # Dark Blue Background
            tcPr = t._tc.get_or_add_tcPr()
            shd = get_or_add_child(tcPr, 'w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:fill'), '1F4E79')
            p = t.paragraphs[0]
            if p.runs:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            
        issue_id_map = {}
        for idx, ((issue_type, details), count) in enumerate(sorted_freq):
             issue_id_map[(issue_type, details)] = idx + 1
             row = table.add_row().cells
             row[0].text = f"[{idx + 1}]"
             row[1].text = issue_type
             row[2].text = details
             row[3].text = str(count)
             for j in range(4):
                 self._style_body_cell(row[j])








        self.doc.add_heading('Discrepancy Details', 1)
        
        # Group issues by endpoint for better flow
        grouped_issues = {}
        for issue in self.issues:
             key = f"{issue.method} {issue.path}"
             if key not in grouped_issues:
                  grouped_issues[key] = []
             grouped_issues[key].append(issue)

        def _format_item_name(name: str) -> str:
             if not name: return "-"
             parts = name.split('.')
             res = []
             for i, p in enumerate(parts):
                 res.append("  " * i + p)
             return "\n".join(res)

        for endpoint, issues in sorted(grouped_issues.items(), key=lambda x: (x[0].split()[1], x[0].split()[0])):
             self.doc.add_heading(endpoint, 2)
             
             # Group by (location, item_name)
             dedup = {}
             dedup = {}
             for issue in issues:
                  k = (issue.location, issue.item_name)
                  if k not in dedup:
                       dedup[k] = []
                  pair = (issue.issue_type, issue.details)
                  if pair not in dedup[k]:
                       dedup[k].append(pair)
             widths = [Inches(1.25), Inches(1.75), Inches(1.25), Inches(2.75)]
             table = self._create_table(4, widths)
             self._add_all_borders(table)
             
             # Headers
             headers = ['Location/Scope', 'Property/Param', 'Issue Type', 'Details']
             hdr_cells = table.rows[0].cells
             self._set_repeat_header(table.rows[0])
             for i, h in enumerate(headers):
                 hdr_cells[i].text = h
                 tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
                 shd = get_or_add_child(tcPr, 'w:shd')
                 shd.set(qn('w:val'), 'clear')
                 shd.set(qn('w:fill'), '1F4E79')
                 p = hdr_cells[i].paragraphs[0]
                 p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                 if p.runs:
                     p.runs[0].font.bold = True
                     p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

             # Rows
             for (loc, item), data in dedup.items():
                  row_cells = table.add_row().cells
                  row_cells[0].text = loc
                  row_cells[1].text = _format_item_name(item)
                  types_strs = []
                  details_strs = []
                  for (it, det) in data:
                       map_idx = issue_id_map.get((it, det), "")
                       idx_str = f"[{map_idx}]" if map_idx else ""
                       types_strs.append(f"{it}")
                       details_strs.append(f"[{map_idx}] {det}")

                  types_strs = list(dict.fromkeys(types_strs))
                  # Issue Type (column 2)
                  if types_strs:
                      p_it = row_cells[2].paragraphs[0]
                      p_it.text = types_strs[0]
                      for t in types_strs[1:]:
                           row_cells[2].add_paragraph(t)
                       
                  # Details (column 3)
                  if details_strs:
                      p_det = row_cells[3].paragraphs[0]
                      p_det.text = details_strs[0]
                      p_det.paragraph_format.left_indent = Inches(0.22)
                      p_det.paragraph_format.first_line_indent = Inches(-0.22)
                      for d in details_strs[1:]:
                           p = row_cells[3].add_paragraph(d)
                           p.paragraph_format.left_indent = Inches(0.22)
                           p.paragraph_format.first_line_indent = Inches(-0.22)
















        self.doc.save(output_path)

    def _add_all_borders(self, table):
        tbl = table._tbl
        tblPr = tbl.tblPr
        tblBorders = get_or_add_child(tblPr, 'w:tblBorders', TBL_PR_ORDER)
        for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            border = get_or_add_child(tblBorders, f'w:{border_name}')
            border.set(qn('w:val'), 'single')
            border.set(qn('w:sz'), '4')
            border.set(qn('w:color'), '000000')

    def _create_table(self, cols, widths):
        table = self.doc.add_table(rows=1, cols=cols)
        self._remove_all_borders(table)
        
        total_width = sum(w.inches for w in widths)
        self._set_table_fixed_width(table, total_width)
        table.alignment = WD_TABLE_ALIGNMENT.LEFT
        
        tblPr = table._tblPr
        tblGrid = table._element.find(qn('w:tblGrid'))
        if tblGrid is None:
            tblGrid = OxmlElement('w:tblGrid')
            table._element.insert(table._element.index(tblPr) + 1, tblGrid)
        else:
            tblGrid.clear()
            
        for w in widths:
            col = OxmlElement('w:gridCol')
            col.set(qn('w:w'), str(int(w.twips)))
            tblGrid.append(col)
            
        for i, cell in enumerate(table.rows[0].cells):
            cell.width = widths[i]
            
        return table

    def _remove_all_borders(self, table):
        tbl = table._tbl
        tblPr = tbl.tblPr
        tblBorders = get_or_add_child(tblPr, 'w:tblBorders', TBL_PR_ORDER)
        for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            border = get_or_add_child(tblBorders, f'w:{border_name}')
            border.set(qn('w:val'), 'nil')

    def _set_table_fixed_width(self, table, width_inches):
        tbl = table._tbl
        tblPr = tbl.tblPr
        tblW = get_or_add_child(tblPr, 'w:tblW', TBL_PR_ORDER)
        tblW.set(qn('w:w'), str(int(width_inches * 1440)))
        tblW.set(qn('w:type'), 'dxa')
        tblLayout = get_or_add_child(tblPr, 'w:tblLayout', TBL_PR_ORDER)
        tblLayout.set(qn('w:type'), 'fixed')

    def _style_body_cell(self, cell):
        # Horizontal Border Only (Light Grey)
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = get_or_add_child(tcPr, 'w:tcBorders', TC_PR_ORDER)
        for side in ['top', 'left', 'right']:
            tag = get_or_add_child(tcBorders, f'w:{side}')
            tag.set(qn('w:val'), 'nil')
        bottom = get_or_add_child(tcBorders, 'w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '4')
        bottom.set(qn('w:color'), 'E0E0E0')

    def _add_metadata_table(self):
        widths = [Inches(1.5), Inches(2.75), Inches(2.75)]
        table = self._create_table(3, widths)
        # Custom Header Styling (Dark Blue Background, White Text)
        headers = ['Detail', 'Old Specification', 'New Specification']
        row = table.rows[0]
        
        for i, text in enumerate(headers):
             cell = row.cells[i]
             cell.text = text
             p = cell.paragraphs[0]
             if p.runs:
                 p.runs[0].font.bold = True
                 p.runs[0].font.color.rgb = RGBColor(255, 255, 255) # White
             
             # Dark Blue Background
             tcPr = cell._tc.get_or_add_tcPr()
             shd = get_or_add_child(tcPr, 'w:shd')
             shd.set(qn('w:val'), 'clear')
             shd.set(qn('w:fill'), '1F4E79') # Dark Blue

             # Bottom border for header like analytic report
             tcBorders = get_or_add_child(tcPr, 'w:tcBorders')
             bottom = get_or_add_child(tcBorders, 'w:bottom')
             bottom.set(qn('w:val'), 'single')
             bottom.set(qn('w:sz'), '12')
             bottom.set(qn('w:color'), 'FFFFFF')

        def get_info(spec, path):
             info = spec.get('info', {}) if isinstance(spec, dict) else {}
             return {
                 'file': os.path.basename(path) if path else "N/A",
                 'title': info.get('title', 'N/A'),
                 'version': str(info.get('version', 'N/A'))
             }
             
        old_info = get_info(self.spec1, self.old_path)
        new_info = get_info(self.spec2, self.new_path)

        rows = [
             ("File Name", old_info['file'], new_info['file']),
             ("API Title", old_info['title'], new_info['title']),
             ("Version", old_info['version'], new_info['version'])
        ]
        
        for d, o, n in rows:
             r_cells = table.add_row().cells
             r_cells[0].text = d
             r_cells[1].text = o
             r_cells[2].text = n
             if r_cells[0].paragraphs:
                 r_cells[0].paragraphs[0].runs[0].font.bold = True
             for j in range(3):
                 self._style_body_cell(r_cells[j])
