"""Analyze styles in existing Excel templates to replicate in generated files."""
import zipfile
import os
from xml.etree import ElementTree as ET

def analyze_styles(filepath):
    """Extract style information from xlsm/xlsx file."""
    ns = {
        'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    }
    
    styles_info = {
        'fonts': [],
        'fills': [],
        'borders': [],
        'cellStyles': []
    }
    
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            # Read styles.xml
            if 'xl/styles.xml' in z.namelist():
                content = z.read('xl/styles.xml')
                root = ET.fromstring(content)
                
                # Count fonts
                fonts = root.find('main:fonts', ns)
                if fonts is not None:
                    styles_info['fonts_count'] = len(list(fonts))
                
                # Count fills
                fills = root.find('main:fills', ns)
                if fills is not None:
                    styles_info['fills_count'] = len(list(fills))
                    # Get fill colors
                    for fill in fills:
                        pattern = fill.find('main:patternFill', ns)
                        if pattern is not None:
                            fg = pattern.find('main:fgColor', ns)
                            if fg is not None and 'rgb' in fg.attrib:
                                styles_info['fills'].append(fg.attrib['rgb'])
                
                # Count borders
                borders = root.find('main:borders', ns)
                if borders is not None:
                    styles_info['borders_count'] = len(list(borders))
                
                # Count cell styles
                cellStyleXfs = root.find('main:cellStyleXfs', ns)
                if cellStyleXfs is not None:
                    styles_info['cellStyleXfs_count'] = len(list(cellStyleXfs))
                
                # Cell formats used
                cellXfs = root.find('main:cellXfs', ns)
                if cellXfs is not None:
                    styles_info['cellXfs_count'] = len(list(cellXfs))
            
            # Check for specific sheet styles
            for name in z.namelist():
                if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
                    sheet_content = z.read(name)
                    sheet_root = ET.fromstring(sheet_content)
                    
                    # Check if sheet has styled rows
                    sheet_data = sheet_root.find('main:sheetData', ns)
                    if sheet_data:
                        styled_rows = 0
                        for row in sheet_data.findall('main:row', ns):
                            if 's' in row.attrib:  # s attribute = style index
                                styled_rows += 1
                        if styled_rows > 0:
                            styles_info.setdefault('sheets_with_row_styles', []).append(name)
                    
    except Exception as e:
        return {'error': str(e)}
    
    return styles_info

def main():
    templates_dir = 'API Templates'
    
    print("=" * 70)
    print("STYLE ANALYSIS FOR OASIS TEMPLATES")
    print("=" * 70)
    
    # Analyze $index.xlsm
    index_file = os.path.join(templates_dir, '$index.xlsm')
    if os.path.exists(index_file):
        print(f"\n$index.xlsm:")
        result = analyze_styles(index_file)
        for key, value in result.items():
            print(f"  {key}: {value}")
    
    # Analyze one operation file
    op_file = os.path.join(templates_dir, 'account_assessment.251111.xlsm')
    if os.path.exists(op_file):
        print(f"\naccount_assessment.251111.xlsm:")
        result = analyze_styles(op_file)
        for key, value in result.items():
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATION: Extract styles.xml and use as template for openpyxl")
    print("=" * 70)

if __name__ == '__main__':
    main()
