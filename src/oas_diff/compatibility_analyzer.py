from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .comparator import _unwrap_schema

@dataclass
class CompatibilityIssue:
    path: str
    method: str
    location: str # Parameter, Request Body, Response 200, Response Header
    item_name: str # Parameter Name, Property Path (e.g. data.user.id)
    issue_type: str # Missing, Added, Type Mismatch, Constraint Mismatch
    details: str
    severity: str = "HIGH" # Can be added for sorting

class CompatibilityAnalyzer:
    """
    Compares fully resolved OpenAPI paths to verify constraint identity
    and report differences in parameters, payloads, and response headers.
    """
    def __init__(self, resolved_spec1: Dict[str, Any], resolved_spec2: Dict[str, Any]):
        self.spec1 = resolved_spec1
        self.spec2 = resolved_spec2
        self.issues: List[CompatibilityIssue] = []

    def analyze(self) -> List[CompatibilityIssue]:
        self.issues = []
        
        # Compare paths present in both specs
        common_paths = set(self.spec1.keys()) & set(self.spec2.keys())
        for path in common_paths:
            self._analyze_path(path, self.spec1[path], self.spec2[path])
            
        return self.issues

    def _analyze_path(self, path: str, path_item1: Dict, path_item2: Dict):
        methods = ['get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'trace']
        
        for method in methods:
            if method in path_item1 and method in path_item2:
                self._analyze_operation(path, method.upper(), path_item1[method], path_item2[method])

    def _analyze_operation(self, path: str, method: str, op1: Dict, op2: Dict):
        # 1. Compare Parameters
        self._compare_parameters(path, method, op1.get('parameters', []), op2.get('parameters', []))
        
        # 2. Compare Request Body
        if 'requestBody' in op1 and 'requestBody' in op2:
            self._compare_request_body(path, method, op1['requestBody'], op2['requestBody'])
        elif 'requestBody' in op1:
             self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Removed", "Request body was removed in new spec."))
        elif 'requestBody' in op2:
             self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Added", "Request body was added in new spec."))

        # 3. Compare Responses
        old_resp = op1.get('responses', {})
        new_resp = op2.get('responses', {})
        common_codes = set(old_resp.keys()) & set(new_resp.keys())
        
        for code in common_codes:
            self._compare_response(path, method, code, old_resp[code], new_resp[code])

    def _compare_parameters(self, path: str, method: str, params1: List[Dict], params2: List[Dict]):
        # Map parameters to unique keys: (name, location)
        def get_param_map(params):
            return {(p.get('name'), p.get('in')): p for p in params}

        map1 = get_param_map(params1)
        map2 = get_param_map(params2)

        for (name, location) in set(map1.keys()) & set(map2.keys()):
            p1 = map1[(name, location)]
            p2 = map2[(name, location)]
            
            # Compare basic parameter fields
            if p1.get('required') != p2.get('required'):
                 self.issues.append(CompatibilityIssue(path, method, f"Parameter ({location})", name, "Constraint Mismatch", f"Property 'required' changed from {p1.get('required')} to {p2.get('required')}"))
            
            # Compare schemas
            if 'schema' in p1 and 'schema' in p2:
                 self._compare_schemas(path, method, f"Parameter ({location})", p1['schema'], p2['schema'], name)

    def _compare_request_body(self, path: str, method: str, rb1: Dict, rb2: Dict):
        # Compare required attribute
        req1 = rb1.get('required', False)
        req2 = rb2.get('required', False)
        if req1 != req2:
             self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Constraint Mismatch", f"Property 'required' changed from {req1} to {req2}"))


        content1 = rb1.get('content', {})
        content2 = rb2.get('content', {})
        common_content = set(content1.keys()) & set(content2.keys())

        
        for media_type in common_content:
             self._compare_schemas(path, method, f"Request Body ({media_type})", content1[media_type].get('schema', {}), content2[media_type].get('schema', {}), "")

    def _compare_response(self, path: str, method: str, code: str, resp1: Dict, resp2: Dict):
        # Header comparison inside responses
        headers1 = resp1.get('headers', {})
        headers2 = resp2.get('headers', {})
        common_headers = set(headers1.keys()) & set(headers2.keys())
        
        for h in common_headers:
            # Headers schema or type and constraints
            s1 = headers1[h].get('schema', {}) if isinstance(headers1[h], dict) else {}
            s2 = headers2[h].get('schema', {}) if isinstance(headers2[h], dict) else {}
            self._compare_schemas(path, method, f"Response {code} Header", s1, s2, h)

        content1 = resp1.get('content', {})
        content2 = resp2.get('content', {})
        common_content = set(content1.keys()) & set(content2.keys())
        
        for media_type in common_content:
             self._compare_schemas(path, method, f"Response {code} ({media_type})", content1[media_type].get('schema', {}), content2[media_type].get('schema', {}), "")

    def _compare_schemas(self, path: str, method: str, location: str, s1: Dict, s2: Dict, item_name_prefix: str, visited=None):
        """
        Deeply compares two resolved schemas and collects constraint mismatches.
        """
        if visited is None: visited = set()
        
        s1 = _unwrap_schema(s1)
        s2 = _unwrap_schema(s2)
        
        # Cycle detection
        pair_id = (id(s1), id(s2))
        if pair_id in visited:
            return
        visited.add(pair_id)

        if not isinstance(s1, dict) or not isinstance(s2, dict):
            if s1 != s2:
                self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Value Mismatch", f"Value changed from {s1} to {s2}"))
            return

        # 1. Compare Core Constraints
        constraints = ['type', 'format', 'minLength', 'maxLength', 'pattern', 'minimum', 'maximum', 'enum']
        for c in constraints:
            v1 = s1.get(c)
            v2 = s2.get(c)
            if v1 != v2:
                # Normalizing none values
                if v1 is None and v2 is None: continue
                
                # Special Case: Enum Order
                if c == 'enum' and isinstance(v1, list) and isinstance(v2, list):
                    if set(v1) == set(v2):
                        self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Enum values order changed", f"Constraint 'enum' changed from {v1} to {v2}", severity="INFO"))
                        continue
                        
                self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Constraint Mismatch", f"Constraint '{c}' changed from {v1} to {v2}"))

        # 2. Compare Properties (Recursive)
        props1 = s1.get('properties', {})
        props2 = s2.get('properties', {})
        
        removed_names = [p for p in props1.keys() if p not in props2]
        added_names = [p for p in props2.keys() if p not in props1]
        common_names = [p for p in props1.keys() if p in props2]
        
        # Match renamed properties (Identical dictionary structures)
        renamed_pairs = {}
        for r_prop in list(removed_names):
            r_def = props1[r_prop]
            for a_prop in list(added_names):
                a_def = props2[a_prop]
                if r_def == a_def: # Identical dicts
                    renamed_pairs[r_prop] = a_prop
                    removed_names.remove(r_prop)
                    added_names.remove(a_prop)
                    break
                    
        for prop in removed_names:
            prop_path = f"{item_name_prefix}.{prop}" if item_name_prefix else prop
            self.issues.append(CompatibilityIssue(path, method, location, prop_path, "Removed", "Property removed in new spec."))
            
        for prop in added_names:
            prop_path = f"{item_name_prefix}.{prop}" if item_name_prefix else prop
            self.issues.append(CompatibilityIssue(path, method, location, prop_path, "Added", "Property added in new spec."))
            
        for r_prop, a_prop in renamed_pairs.items():
            prop_path_old = f"{item_name_prefix}.{r_prop}" if item_name_prefix else r_prop
            self.issues.append(CompatibilityIssue(path, method, location, prop_path_old, "Renamed", f"Property renamed to '{a_prop}' in new spec."))
            
        for prop in common_names:
            prop_path = f"{item_name_prefix}.{prop}" if item_name_prefix else prop
            self._compare_schemas(path, method, location, props1[prop], props2[prop], prop_path, visited)


        # 3. Compare Items (Arrays)
        if 'items' in s1 and 'items' in s2:
             self._compare_schemas(path, method, location, s1['items'], s2['items'], f"{item_name_prefix}[]", visited)
        elif 'items' in s1:
             self.issues.append(CompatibilityIssue(path, method, location, f"{item_name_prefix}[]", "Removed", "Array item definition removed in new spec."))
        elif 'items' in s2:
             self.issues.append(CompatibilityIssue(path, method, location, f"{item_name_prefix}[]", "Added", "Array item definition added in new spec."))
