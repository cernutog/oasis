import yaml

def analyze_headers():
    try:
        with open(r'Expected results\EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml', 'r', encoding='utf-8') as f:
            gold = yaml.safe_load(f)
        with open(r'Roundtrip_Output\generated_oas_3.1.yaml', 'r', encoding='utf-8') as f:
            gen = yaml.safe_load(f)
            
        path = '/v1/accounts/assessments/vop'
        method = 'post'
        code = 201 # check both int and str keys
        
        # Helper to get response
        def get_resp(oas_dict):
            paths = oas_dict.get('paths', {})
            op = paths.get(path, {}).get(method, {})
            responses = op.get('responses', {})
            return responses.get(code) or responses.get(str(code)) or {}

        resp_g = get_resp(gold)
        resp_n = get_resp(gen)
        
        h_g = resp_g.get('headers', {})
        h_n = resp_n.get('headers', {})
        
        print(f'=== HEADERS ANALYSIS for {path} {method} {code} ===')
        print(f'Gold headers count: {len(h_g)}')
        print(f'Gen headers count: {len(h_n)}')
        
        print('\n--- GOLD HEADERS ---')
        for k, v in h_g.items():
            print(f'{k}: {v}')
            
        print('\n--- GEN HEADERS ---')
        for k, v in h_n.items():
            print(f'{k}: {v}')
            
        # Missing headers
        missing = set(h_g.keys()) - set(h_n.keys())
        if missing:
            print(f'\nMISSING IN GEN: {missing}')
            
    except Exception as e:
        print(f'Error analyzing headers: {e}')

if __name__ == '__main__':
    analyze_headers()
