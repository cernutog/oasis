import os
from .oas_parser import OASParser

class OASComparator:
    """
    Compares two OAS files (Gold/Original vs Generated) 
    to validate roundtrip fidelity.
    """
    
    def __init__(self, gold_path: str, gen_path: str):
        self.gold_path = gold_path
        self.gen_path = gen_path
        self.gold_oas = OASParser(gold_path).oas
        self.gen_oas = OASParser(gen_path).oas
        
    def get_structure_comparison(self) -> dict:
        """
        Returns a dictionary comparing ITEM COUNTS of top-level OAS sections.
        """
        metrics = {}
        
        # 1. Info (Single object)
        metrics['Info'] = (1 if self.gold_oas.get('info') else 0, 1 if self.gen_oas.get('info') else 0)
        
        # 2. Servers (List count)
        g_servers = self.gold_oas.get('servers', [])
        t_servers = self.gen_oas.get('servers', [])
        metrics['Servers'] = (len(g_servers), len(t_servers))
        
        # 3. Tags (List count)
        g_tags = self.gold_oas.get('tags', [])
        t_tags = self.gen_oas.get('tags', [])
        metrics['Tags'] = (len(g_tags), len(t_tags))
        
        # 4. Paths (Key count)
        g_paths = self.gold_oas.get('paths', {})
        t_paths = self.gen_oas.get('paths', {})
        metrics['Paths'] = (len(g_paths), len(t_paths))
        
        # 5. Components (Total count of all sub-components)
        g_comps = self.gold_oas.get('components', {})
        t_comps = self.gen_oas.get('components', {})
        
        def count_components(comp_dict):
            total = 0
            for k, v in comp_dict.items():
                if isinstance(v, dict):
                    total += len(v)
            return total

        metrics['Components'] = (count_components(g_comps), count_components(t_comps))
        
        # 6. Security (List count)
        g_sec = self.gold_oas.get('security', [])
        t_sec = self.gen_oas.get('security', [])
        metrics['Security'] = (len(g_sec), len(t_sec))
        
        return metrics
    
    def get_detailed_structure_breakdown(self) -> dict:
        """
        Returns detailed ITEMS count breakdown.
        """
        breakdown = {}
        
        # Components breakdown by subsection
        g_comps = self.gold_oas.get('components', {})
        t_comps = self.gen_oas.get('components', {})
        
        comp_details = {}
        # Expand list to include ALL component types
        comp_types = ['schemas', 'parameters', 'responses', 'headers', 
                      'requestBodies', 'securitySchemes', 'links', 'callbacks', 'examples']
                      
        for key in comp_types:
            g_section = g_comps.get(key, {}) or {}
            t_section = t_comps.get(key, {}) or {}
            
            g_count = len(g_section)
            t_count = len(t_section)
            
            if g_count > 0 or t_count > 0:
                comp_details[key] = (g_count, t_count, t_count - g_count)
        
        breakdown['components'] = comp_details
        
        # Paths breakdown - Still useful to find BIGGEST discrepancies in loops/logic
        # For paths, we might want to check OPERATION counts per path?
        # Or stick to Line Diff for "Top 10 Discrepancies" because that highlights content changes?
        # User asked for "breakdown... anche per tutte le altre strutture".
        # Let's keep Paths Discrepancy based on Line Count (proxy for modification) 
        # but explicitly label it as "Line Delta" in the UI if possible, or just keep it as is
        # since it's a "Top 10 Discrepancies" list.
        
        # Actually, let's switch Paths breakdown to be purely about "Missing/Added" paths if possible?
        # No, "discrepancies" usually implies content mismatch.
        # Let's keep the Line Count Delta logic for Paths Breakdown as it acts as a heuristic for content change,
        # BUT we must clarify it.
        # Wait, the user said "tutte le altre strutture".
        # I have added full components breakdown.
        
        g_paths = self.gold_oas.get('paths', {})
        t_paths = self.gen_oas.get('paths', {})
        
        path_details = []
        import yaml
        
        # Union of all paths
        all_paths = set(list(g_paths.keys()) + list(t_paths.keys()))
        
        for path_name in all_paths:
            g_path_obj = g_paths.get(path_name)
            t_path_obj = t_paths.get(path_name)
            
            # If path is missing
            if g_path_obj is None:
                # Added
                t_lines = len(str(t_path_obj).splitlines()) # Approximate or use yaml dump
                path_details.append((path_name, 0, 1, 1)) # 0 vs 1 (Present)
                continue
            if t_path_obj is None:
                # Removed
                path_details.append((path_name, 1, 0, -1))
                continue
                
            # Both exist - compare content size (lines) to find changes
            def count_yaml_lines(obj):
                if not obj: return 0
                return len(yaml.dump(obj, default_flow_style=False, sort_keys=False).strip().split('\n'))
            
            g_lines = count_yaml_lines(g_path_obj)
            t_lines = count_yaml_lines(t_path_obj)
            delta = t_lines - g_lines
            
            if delta != 0:
                path_details.append((path_name, g_lines, t_lines, delta))
        
        # Sort by absolute delta
        path_details.sort(key=lambda x: abs(x[3]), reverse=True)
        breakdown['paths'] = path_details  # All discrepancies
        
        return breakdown

    def get_line_comparison(self) -> dict:
        """
        Returns line count comparison.
        """
        def count_lines(path):
            if not os.path.exists(path):
                return 0
            with open(path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
                
        g_lines = count_lines(self.gold_path)
        t_lines = count_lines(self.gen_path)
        
        return {'Total Lines': (g_lines, t_lines)}

    def get_line_diff_stats(self) -> dict:
        """
        Returns stats on line differences.
        Format: {'Added': count, 'Removed': count}
        """
        import difflib
        
        with open(self.gold_path, 'r', encoding='utf-8') as f:
            g_lines = f.readlines()
        with open(self.gen_path, 'r', encoding='utf-8') as f:
            t_lines = f.readlines()
            
        diff = list(difflib.unified_diff(g_lines, t_lines, n=0))
        
        added = 0
        removed = 0
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                added += 1
            elif line.startswith('-') and not line.startswith('---'):
                removed += 1
                
        return {'Added Lines': added, 'Removed Lines': removed}

    def get_detailed_line_diff(self) -> list:
        """
        Returns a diff of lines (using difflib).
        Expensive operation, only call if requested.
        """
        import difflib
        
        with open(self.gold_path, 'r', encoding='utf-8') as f:
            g_lines = f.readlines()
        with open(self.gen_path, 'r', encoding='utf-8') as f:
            t_lines = f.readlines()
            
        diff = difflib.unified_diff(
            g_lines, t_lines, 
            fromfile='Source OAS', 
            tofile='Generated OAS',
            n=0 # Minimal context
        )
        return list(diff)

    def get_component_discrepancies(self) -> dict:
        """
        Returns a dictionary of discrepancies for EACH component type.
        Format: {'schemas': [(name, src_lines, gen_lines, delta), ...], ...}
        Only includes items with non-zero delta.
        """
        import yaml
        discrepancies = {}
        
        g_comps = self.gold_oas.get('components', {})
        t_comps = self.gen_oas.get('components', {})
        
        comp_types = ['schemas', 'parameters', 'responses', 'headers', 
                      'requestBodies', 'securitySchemes', 'links', 'callbacks', 'examples']
                      
        for c_type in comp_types:
            g_section = g_comps.get(c_type, {}) or {}
            t_section = t_comps.get(c_type, {}) or {}
            
            type_diffs = []
            all_keys = set(list(g_section.keys()) + list(t_section.keys()))
            
            for name in all_keys:
                g_obj = g_section.get(name)
                t_obj = t_section.get(name)
                
                if g_obj is None:
                    # Added
                    t_lines = len(yaml.dump(t_obj, default_flow_style=False, sort_keys=False).strip().split('\n'))
                    type_diffs.append((name, 0, t_lines, t_lines))
                    continue
                if t_obj is None:
                    # Removed
                    g_lines = len(yaml.dump(g_obj, default_flow_style=False, sort_keys=False).strip().split('\n'))
                    type_diffs.append((name, g_lines, 0, -g_lines))
                    continue
                    
                # Content Check via line count proxy
                def count_lines(obj):
                     if not obj: return 0
                     return len(yaml.dump(obj, default_flow_style=False, sort_keys=False).strip().split('\n'))
                
                g_lines = count_lines(g_obj)
                t_lines = count_lines(t_obj)
                delta = t_lines - g_lines
                
                if delta != 0:
                    type_diffs.append((name, g_lines, t_lines, delta))
            
            if type_diffs:
                type_diffs.sort(key=lambda x: abs(x[3]), reverse=True)
                discrepancies[c_type] = type_diffs
        
        return discrepancies

    def _format_path(self, parent, key):
        """Standardize path formatting for reporting (single slash)."""
        if not parent:
            return key
        p = parent.rstrip("/")
        k = key.lstrip("/")
        return f"{p}/{k}"

    def _has_semantic_content(self, obj, key=None):
        """
        Recursively checks if an object has meaningful content.
        Significant leaves (like operations) are content even if empty.
        Noise containers (like 'headers' blocks) are only content if they have non-noise children.
        """
        if not isinstance(obj, (dict, list)):
            return True # Primitives are always content
        
        if not obj:
            # Empty container. Is it significant?
            k_lower = str(key).lower() if key else ""
            always_significant = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
            if k_lower in always_significant:
                return True
            
            # Known noise blocks
            noise_containers = {"headers", "parameters", "responses", "schemas", 
                                "securityschemes", "tags", "servers", "security", "properties"}
            if k_lower in noise_containers:
                return False
            
            # Default for other empty containers (e.g. empty component names)
            return False 

        # Non-empty container: check children
        if isinstance(obj, dict):
            return any(self._has_semantic_content(v, k) for k, v in obj.items())
        return any(self._has_semantic_content(v) for v in obj)

    def _is_noise(self, path):
        """Returns True if the path points to an auto-generated or irrelevant attribute."""
        noise_keys = [
            "x-info-creation-date", 
            "x-info-release", 
            "info/version"
        ]
        return any(path.endswith(key) for key in noise_keys)

    def _is_equivalent(self, val1, val2):
        """
        Aggressively treats None, empty strings, and whitespace-only strings as identical.
        Also strips trailing spaces from each line in multi-line strings.
        """
        def _normalize(v):
            if v is None:
                return ""
            # Split into lines, strip trailing whitespace from each, rejoin
            lines = str(v).splitlines()
            cleaned = "\n".join(line.rstrip() for line in lines)
            return cleaned.strip()
        
        s1 = _normalize(val1)
        s2 = _normalize(val2)
        
        # Normalize common empty-like values
        if s1.lower() in ["", "none", "nan"]: s1 = ""
        if s2.lower() in ["", "none", "nan"]: s2 = ""
        
        return s1 == s2

    def get_attribute_diff(self) -> dict:
        """
        Deep comparison of attributes between Source and Generated OAS.
        Returns categorized results.
        """
        raw_results = {
            "added": [],    # Paths present in Generated but not in Source
            "removed": [],   # Paths present in Source but not in Generated
            "modified": []   # Values differ between Source and Generated
        }
        
        self._compare_structures(self.gold_oas, self.gen_oas, "", raw_results)
        
        # Categorize results
        categorized = {
            "Info": {"added": [], "removed": [], "modified": []},
            "Paths": {"added": [], "removed": [], "modified": []},
            "Components": {"added": [], "removed": [], "modified": []},
            "Security": {"added": [], "removed": [], "modified": []},
            "Other": {"added": [], "removed": [], "modified": []}
        }
        
        for action in ["added", "removed", "modified"]:
            for item in raw_results[action]:
                # Handle both plain strings (added/removed) and dicts (modified)
                path = item["path"] if isinstance(item, dict) else item
                p_lower = path.lower()
                
                if p_lower.startswith("info"):
                    categorized["Info"][action].append(item)
                elif p_lower.startswith("paths"):
                    categorized["Paths"][action].append(item)
                elif p_lower.startswith("components"):
                    categorized["Components"][action].append(item)
                elif p_lower.startswith("security"):
                    categorized["Security"][action].append(item)
                else:
                    categorized["Other"][action].append(item)
                    
        return categorized

    def _compare_structures(self, gold, gen, path, results):
        """
        Recursive helper to compare dictionaries and lists.
        """
        if isinstance(gold, dict) and isinstance(gen, dict):
            # Compare Keys
            gold_keys = set(gold.keys())
            gen_keys = set(gen.keys())
            
            # Removed from Source
            for k in gold_keys - gen_keys:
                full_path = self._format_path(path, k)
                if self._is_noise(full_path):
                    continue
                
                # Check if this removal has any semantic content.
                # If we are removing an empty block like 'headers: {}', it's not a real discrepancy.
                if not self._has_semantic_content(gold[k], k):
                    continue
                    
                results["removed"].append(full_path)
            
            # Added to Generated
            for k in gen_keys - gold_keys:
                full_path = self._format_path(path, k)
                if self._is_noise(full_path):
                    continue
                
                # Check if this addition has any semantic content recursively.
                if not self._has_semantic_content(gen[k], k):
                    continue
                    
                results["added"].append(full_path)
                
            # Recursively compare common keys
            for k in gold_keys & gen_keys:
                full_path = self._format_path(path, k)
                self._compare_structures(gold[k], gen[k], full_path, results)
                
        elif isinstance(gold, list) and isinstance(gen, list):
            # Special handling for lists like parameters, tags, etc.
            # We try to match items by specific keys
            
            # 0. REQUIRED (treat as set - order doesn't matter)
            if path.endswith("/required"):
                self._compare_required_as_set(gold, gen, path, results)
            
            # 1. PARAMETERS (Match by name + in)
            elif "parameters" in path.lower():
                self._compare_keyed_lists(gold, gen, path, results, ["name", "in"])
            
            # 2. TAGS (Match by name)
            elif "tags" in path.lower() and (path == "tags" or path.endswith("/tags")):
                self._compare_keyed_lists(gold, gen, path, results, ["name"])
            
            # 3. SECURITY (Match by keys of dict items)
            elif "security" in path.lower():
                 self._compare_security_lists(gold, gen, path, results)
            
            # 4. GENERIC LISTS (oneOf, anyOf, enum, etc.) - RECURSIVE
            else:
                self._compare_generic_lists(gold, gen, path, results)
        
        elif not self._is_equivalent(gold, gen):
            # Value mismatch
            if not self._is_noise(path):
                results["modified"].append({
                    "path": path,
                    "old": str(gold),
                    "new": str(gen)
                })

    def _compare_keyed_lists(self, gold_list, gen_list, path, results, key_names):
        """Helper to compare lists of objects using one or more keys for identification."""
        def get_id(obj):
            if not isinstance(obj, dict): return str(obj)
            return "|".join([str(obj.get(kn, "")) for kn in key_names])
            
        gold_map = {get_id(o): o for o in gold_list if isinstance(o, dict)}
        gen_map = {get_id(o): o for o in gen_list if isinstance(o, dict)}
        
        gold_ids = set(gold_map.keys())
        gen_ids = set(gen_map.keys())
        
        # Missing items
        for gid in gold_ids - gen_ids:
            results["removed"].append(f"{path}[{gid}]")
            
        # Added items
        for gid in gen_ids - gold_ids:
            results["added"].append(f"{path}[{gid}]")
            
        # Recursive compare common items
        for gid in gold_ids & gen_ids:
            self._compare_structures(gold_map[gid], gen_map[gid], f"{path}[{gid}]", results)

    def _compare_security_lists(self, gold_list, gen_list, path, results):
        """Special handling for security requirement lists."""
        def get_sec_id(obj):
            if not isinstance(obj, dict): return str(obj)
            keys = sorted(obj.keys())
            return ",".join(keys)
            
        gold_map = {get_sec_id(o): o for o in gold_list}
        gen_map = {get_sec_id(o): o for o in gen_list}
        
        gold_ids = set(gold_map.keys())
        gen_ids = set(gen_map.keys())
        
        for sid in gold_ids - gen_ids:
            results["removed"].append(f"{path}[{sid}]")
        for sid in gen_ids - gold_ids:
            results["added"].append(f"{path}[{sid}]")
        for sid in gold_ids & gen_ids:
            self._compare_structures(gold_map[sid], gen_map[sid], f"{path}[{sid}]", results)

    def _compare_required_as_set(self, gold_list, gen_list, path, results):
        """Compares 'required' arrays as sets - order doesn't matter."""
        gold_set = set(str(x) for x in gold_list)
        gen_set = set(str(x) for x in gen_list)
        
        # Only report if actual content differs
        removed = gold_set - gen_set
        added = gen_set - gold_set
        
        for item in removed:
            results["removed"].append(f"{path}/{item}")
        for item in added:
            results["added"].append(f"{path}/{item}")

    def _compare_generic_lists(self, gold_list, gen_list, path, results):
        """Recursively compares generic lists by index."""
        max_idx = max(len(gold_list), len(gen_list))
        for i in range(max_idx):
            current_path = f"{path}[{i}]"
            
            if i >= len(gold_list):
                # Added in Generated
                if self._has_semantic_content(gen_list[i]):
                     results["added"].append(current_path)
                continue
                
            if i >= len(gen_list):
                # Removed from Source
                if self._has_semantic_content(gold_list[i]):
                    results["removed"].append(current_path)
                continue
                
            # Both exist - recurse
            self._compare_structures(gold_list[i], gen_list[i], current_path, results)

    def _count_operations(self, paths: dict) -> int:
        count = 0
        valid_methods = {'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'}
        for path_item in paths.values():
            for key in path_item:
                if key.lower() in valid_methods:
                    count += 1
        return count
