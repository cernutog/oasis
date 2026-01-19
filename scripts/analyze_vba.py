"""Analyze VBA macros in Excel templates to determine if they are actively used."""
import zipfile
import os
import struct

def analyze_vba_project(filepath):
    """Extract basic info about VBA project from xlsm file."""
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            if 'xl/vbaProject.bin' not in z.namelist():
                return {'has_vba': False, 'size': 0}
            
            vba_content = z.read('xl/vbaProject.bin')
            size = len(vba_content)
            
            # Look for common VBA code patterns in the binary
            code_patterns = [
                b'Sub ',
                b'Function ',
                b'Private Sub',
                b'Public Sub',
                b'Workbook_',
                b'Worksheet_',
                b'MsgBox',
                b'Range(',
                b'Cells(',
            ]
            
            found_patterns = []
            for pattern in code_patterns:
                if pattern in vba_content:
                    found_patterns.append(pattern.decode('utf-8', errors='ignore'))
            
            return {
                'has_vba': True,
                'size': size,
                'patterns': found_patterns
            }
    except Exception as e:
        return {'error': str(e)}

def main():
    templates_dir = 'API Templates'
    
    print("=" * 70)
    print("VBA MACRO ANALYSIS FOR OASIS TEMPLATES")
    print("=" * 70)
    
    all_patterns = set()
    
    for f in sorted(os.listdir(templates_dir)):
        if f.endswith('.xlsm') and not f.startswith('~$'):
            filepath = os.path.join(templates_dir, f)
            result = analyze_vba_project(filepath)
            
            print(f"\n{f}:")
            if 'error' in result:
                print(f"  ERROR: {result['error']}")
            elif not result['has_vba']:
                print("  No VBA project")
            else:
                print(f"  VBA Size: {result['size']} bytes")
                print(f"  Code patterns found: {result['patterns']}")
                all_patterns.update(result['patterns'])
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"All code patterns found across templates: {sorted(all_patterns)}")
    
    if all_patterns:
        print("\nCONCLUSION: Macros contain code - need further investigation")
    else:
        print("\nCONCLUSION: VBA projects appear to be empty shells - safe to use .xlsx")

if __name__ == '__main__':
    main()
