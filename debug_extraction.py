
from src.v3_parser import V3Parser
import os

def debug_extraction():
    parser = V3Parser("Templates Legacy")
    ir = parser.parse_all()
    op = ir.operations["listAlerts"]
    dt_roots = op.sheets["Data Type"]
    for node in dt_roots:
        if node.name.lower() == "alerts":
            print(f"DEBUG: node={node.name}, type={node.type_literal}, parent={node.parent_name}")
            break

if __name__ == "__main__":
    debug_extraction()
