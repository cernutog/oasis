
import pandas as pd
import os

def inspect_structure():
    master_path = "Templates Master/$index.xlsx"
    converted_path = "Templates Converted V3/$index.xlsx"

    print("--- Analisi Intestazioni Fogli 'Schemas' ---")
    
    if os.path.exists(master_path):
        m_df = pd.read_excel(master_path, "Schemas", header=None)
        print(f"Master (Riga 0): {m_df.iloc[0].to_list()}")
        print(f"Master (Riga 1): {m_df.iloc[1].to_list() if len(m_df) > 1 else 'N/A'}")
    
    if os.path.exists(converted_path):
        c_df = pd.read_excel(converted_path, "Schemas", header=None)
        print(f"\nConvertito (Riga 0): {c_df.iloc[0].to_list()}")
        print(f"Convertito (Riga 1): {c_df.iloc[1].to_list() if len(c_df) > 1 else 'N/A'}")
        
    print("\n--- Analisi Prime Righe Operazione (listAlerts.xlsx) ---")
    op_master = "Templates Master/endpoint.xlsx"
    op_converted = "Templates Converted V3/listAlerts.xlsx"
    
    if os.path.exists(op_master):
        mo_df = pd.read_excel(op_master, "Body", header=None)
        print(f"Master Op (Riga 0): {mo_df.iloc[0].to_list()}")
        print(f"Master Op (Riga 1): {mo_df.iloc[1].to_list()}")
        print(f"Master Op (Riga 2): {mo_df.iloc[2].to_list()}")

    if os.path.exists(op_converted):
        co_df = pd.read_excel(op_converted, "Body", header=None)
        print(f"\nConvertito Op (Riga 0): {co_df.iloc[0].to_list()}")
        print(f"Convertito Op (Riga 1): {co_df.iloc[1].to_list()}")
        print(f"Convertito Op (Riga 2): {co_df.iloc[2].to_list()}")

if __name__ == "__main__":
    inspect_structure()
