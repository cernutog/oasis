
import pandas as pd
import os
import sys

def compare_excel_files(ref_path, gen_path, report_path):
    print(f"Comparing:\nReference: {ref_path}\nGenerated: {gen_path}")
    
    if not os.path.exists(ref_path):
        print(f"ERROR: Reference file not found: {ref_path}")
        return
    if not os.path.exists(gen_path):
        print(f"ERROR: Generated file not found: {gen_path}")
        return

    report = []
    report.append(f"# Index Comparison Report")
    report.append(f"**Reference**: `{ref_path}`")
    report.append(f"**Generated**: `{gen_path}`")
    report.append("")

    try:
        ref_sheets = pd.read_excel(ref_path, sheet_name=None)
        gen_sheets = pd.read_excel(gen_path, sheet_name=None)
    except Exception as e:
        print(f"ERROR reading Excel files: {e}")
        return

    all_sheets = sorted(list(set(ref_sheets.keys()) | set(gen_sheets.keys())))
    
    has_differences = False

    for sheet in all_sheets:
        report.append(f"## Sheet: {sheet}")
        
        in_ref = sheet in ref_sheets
        in_gen = sheet in gen_sheets
        
        if not in_ref:
            report.append("- [ ] **Missing in Reference** (Present only in Generated)")
            has_differences = True
            continue
        if not in_gen:
            report.append("- [ ] **Missing in Generated** (Present only in Reference)")
            has_differences = True
            continue

        df_ref = ref_sheets[sheet]
        df_gen = gen_sheets[sheet]

        # Normalize empty strings and NaNs
        df_ref = df_ref.fillna("").astype(str).map(lambda x: x.strip())
        df_gen = df_gen.fillna("").astype(str).map(lambda x: x.strip())
        
        # Normalize Mandatory field: M/Yes -> M, O/blank/No -> ""
        def normalize_mandatory(val):
            val_lower = val.lower()
            if val_lower in ['m', 'yes', 'y', 'true']:
                return 'M'
            elif val_lower in ['o', 'no', 'n', 'false', '']:
                return ''
            return val
        
        for col in df_ref.columns:
            col_lower = str(col).lower()
            if 'mandatory' in col_lower or 'required' in col_lower:
                df_ref[col] = df_ref[col].map(normalize_mandatory)
                df_gen[col] = df_gen[col].map(normalize_mandatory)
        
        # Check Shape
        if df_ref.shape != df_gen.shape:
             report.append(f"- [ ] **Shape Mismatch**: Ref {df_ref.shape} vs Gen {df_gen.shape}")
             has_differences = True
        
        # Check Columns
        ref_cols = list(df_ref.columns)
        gen_cols = list(df_gen.columns)
        if ref_cols != gen_cols:
             report.append(f"- [ ] **Column Mismatch**:")
             report.append(f"  - Ref: {ref_cols}")
             report.append(f"  - Gen: {gen_cols}")
             has_differences = True
             # Align columns for content check if possible
             common_cols = [c for c in ref_cols if c in gen_cols]
             df_ref = df_ref[common_cols]
             df_gen = df_gen[common_cols]
        
        # Compare Content
        try:
            # Reindex to ensure alignment if shapes differ
            max_rows = max(len(df_ref), len(df_gen))
            df_ref = df_ref.reindex(range(max_rows)).fillna("")
            df_gen = df_gen.reindex(range(max_rows)).fillna("")
            
            diff_mask = df_ref != df_gen
            if diff_mask.any().any():
                report.append("- [ ] **Content Differences**:")
                has_differences = True
                
                # List differing rows
                diff_rows = diff_mask.any(axis=1)
                for idx in diff_rows[diff_rows].index:
                    report.append(f"  - **Row {idx+2}** (Excel Line {idx+2}):")
                    for col in df_ref.columns:
                        val_ref = df_ref.at[idx, col]
                        val_gen = df_gen.at[idx, col]
                        if val_ref != val_gen:
                            # Truncate long values
                            trunc_ref = (val_ref[:50] + '...') if len(val_ref) > 50 else val_ref
                            trunc_gen = (val_gen[:50] + '...') if len(val_gen) > 50 else val_gen
                            report.append(f"    - **{col}**: Reference=`{trunc_ref}` vs Generated=`{trunc_gen}`")
            else:
                report.append("- [x] Content Identical")

        except Exception as e:
             report.append(f"- [ ] **Comparison Error**: {e}")
             has_differences = True
             
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Report generated at: {report_path}")
    if has_differences:
        print("FAIL: Differences found.")
    else:
        print("SUCCESS: Files are identical.")

if __name__ == "__main__":
    ref_file = os.path.join("API Templates", "$index.xlsm")
    gen_file = os.path.join("Imported Templates", "$index.xlsx")
    report_file = "index_comparison_report.md"
    
    # Adjust for test folder execution
    if not os.path.exists("API Templates") and os.path.exists("../API Templates"):
         ref_file = os.path.join("../API Templates", "$index.xlsm")
         gen_file = os.path.join("../Imported Templates", "$index.xlsx")
         
    compare_excel_files(ref_file, gen_file, report_file)
