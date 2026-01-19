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

    def _count_operations(self, paths: dict) -> int:
        count = 0
        valid_methods = {'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'}
        for path_item in paths.values():
            for key in path_item:
                if key.lower() in valid_methods:
                    count += 1
        return count
