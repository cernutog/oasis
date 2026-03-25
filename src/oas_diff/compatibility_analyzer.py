from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from .comparator import _unwrap_schema
import re

@dataclass
class CompatibilityIssue:
    path: str
    method: str
    location: str # Parameter, Request Body, Response 200, Response Header
    item_name: str # Parameter Name, Property Path (e.g. data.user.id)
    issue_type: str # Missing, Added, Type Mismatch, Constraint Mismatch, Description Change
    details: str
    severity: str = "HIGH"
    old_value: Any = None
    new_value: Any = None
    schema_name: str = None

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
            req1 = p1.get('required', False)
            req2 = p2.get('required', False)
            if req1 != req2:
                 self.issues.append(CompatibilityIssue(path, method, f"Parameter ({location})", name, "Constraint Mismatch", f"Property 'required' changed from {req1} to {req2}", old_value=req1, new_value=req2))
            
            # Compare schemas
            if 'schema' in p1 and 'schema' in p2:
                 self._compare_schemas(path, method, f"Parameter ({location})", p1['schema'], p2['schema'], name)

    def _compare_request_body(self, path: str, method: str, rb1: Dict, rb2: Dict):
        # Compare required attribute
        req1 = rb1.get('required', False)
        req2 = rb2.get('required', False)
        if req1 != req2:
             self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Constraint Mismatch", f"Property 'required' changed from {req1} to {req2}", old_value=req1, new_value=req2))


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

    def _compare_schemas(self, path: str, method: str, location: str, s1, s2, item_name_prefix: str, visited=None, skip_description=False):
        """
        Deeply compares two resolved schemas and collects constraint mismatches.
        """
        if visited is None: visited = set()
        
        # RECURSIVE SCHEMA FLATTENING (merges allOf)
        def _flatten(s):
            if not isinstance(s, dict): return s
            if 'allOf' in s:
                merged = {}
                for item in s['allOf']:
                    f_item = _flatten(item)
                    if isinstance(f_item, dict):
                        for k, v in f_item.items():
                            if k == 'properties':
                                merged.setdefault('properties', {}).update(v)
                            elif k == 'required' and isinstance(v, list):
                                reqs = merged.setdefault('required', [])
                                reqs.extend([r for r in v if r not in reqs])
                            else:
                                merged[k] = v
                # Outer sibling properties override allOf content
                for k, v in s.items():
                    if k != 'allOf':
                        if k == 'properties':
                            merged.setdefault('properties', {}).update(v)
                        else:
                            merged[k] = v
                return merged
            return s

        s1 = _flatten(s1)
        s2 = _flatten(s2)
        
        # Avoid infinite recursion (recursive schemas)
        s1_id = id(s1)
        s2_id = id(s2)
        state = (s1_id, s2_id, item_name_prefix)
        if state in visited: return
        visited.add(state)

        if not isinstance(s1, dict) or not isinstance(s2, dict):
            if s1 != s2:
                self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Value Mismatch", f"Value changed from {s1} to {s2}"))
            return

        # 1. Description Logic (Symmetric Array Rule)
        p1 = s1.get('description')
        i1 = s1.get('items', {}).get('description') if s1.get('type') == 'array' else None
        p2 = s2.get('description')
        i2 = s2.get('items', {}).get('description') if s2.get('type') == 'array' else None
        
        has_only_one1 = (p1 is not None) ^ (i1 is not None)
        has_only_one2 = (p2 is not None) ^ (i2 is not None)
        
        skip_desc_recursive = False
        eff1, eff2 = p1, p2
        
        if s1.get('type') == 'array' and s2.get('type') == 'array':
            if has_only_one1 and has_only_one2:
                # Flexible mode: one vs one
                eff1 = p1 or i1
                eff2 = p2 or i2
                skip_desc_recursive = True
            else:
                # Positional mode: p vs p, i vs i
                eff1 = p1
                eff2 = p2
                skip_desc_recursive = False

        # Compare effective descriptions
        def _norm_desc(txt):
            if txt is None: return ''
            # Aggressive normalization: handle newlines, tabs, multiple spaces
            return re.sub(r'\s+', ' ', str(txt)).strip()
        
        if not skip_description:
            if _norm_desc(eff1) != _norm_desc(eff2):
                self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Description Change", "Description changed", old_value=eff1, new_value=eff2))

        # 2. Compare Core Constraints
        constraints = ['type', 'format', 'minLength', 'maxLength', 'pattern', 'enum', 'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum', 'minItems', 'maxItems', 'uniqueItems', 'minProperties', 'maxProperties', 'nullable', 'readOnly', 'writeOnly', 'deprecated']

        for c in constraints:
            v1 = s1.get(c)
            v2 = s2.get(c)
            if v1 is None and v2 is None: continue
            if v1 != v2:
                # Special Case: Enum Order
                if c == 'enum' and isinstance(v1, list) and isinstance(v2, list):
                    if set(v1) == set(v2):
                        self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Enum values order changed", "Constraint 'enum' order changed", severity="INFO", old_value=v1, new_value=v2))
                        continue

                v1_str = f"'{v1}'" if v1 is not None else "<None>"
                v2_str = f"'{v2}'" if v2 is not None else "<None>"
                msg = f"Constraint '{c}' changed from {v1_str} to {v2_str}"
                self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Constraint Mismatch", msg, old_value=v1, new_value=v2))


        # 2. Compare Properties (Recursive)
        props1 = s1.get('properties', {})
        props2 = s2.get('properties', {})
        req1 = s1.get('required', [])
        req2 = s2.get('required', [])
        
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
            
            # Check required at property level
            is_req1 = prop in req1
            is_req2 = prop in req2
            if is_req1 != is_req2:
                self.issues.append(CompatibilityIssue(path, method, location, prop_path, "Constraint Mismatch", f"Property 'required' changed from {is_req1} to {is_req2}", old_value=is_req1, new_value=is_req2))
            
            self._compare_schemas(path, method, location, props1[prop], props2[prop], prop_path, visited)


        # 3. Compare Items (Arrays)
        if 'items' in s1 and 'items' in s2:
             self._compare_schemas(path, method, location, s1['items'], s2['items'], f"{item_name_prefix}[]", visited, skip_description=skip_desc_recursive)
        elif 'items' in s1:
             self.issues.append(CompatibilityIssue(path, method, location, f"{item_name_prefix}[]", "Removed", "Array item definition removed in new spec."))
        elif 'items' in s2:
             self.issues.append(CompatibilityIssue(path, method, location, f"{item_name_prefix}[]", "Added", "Array item definition added in new spec."))
