"""Check parsed response object for inline description."""
from src.oas_importer import OASParser

parser = OASParser(r'Expected results\EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml')
ops = parser.get_operations()

op = ops[0]
print(f'{op.method} {op.path}')
for code, resp in list(op.responses.items())[:3]:
    ref_val = getattr(resp, 'ref', None)
    desc_val = resp.description[:30] if resp.description else None
    print(f'  {code}: ref={ref_val}, desc={desc_val}')
