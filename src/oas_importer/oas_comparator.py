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
        Returns a dictionary comparing LINE COUNTS of top-level OAS sections.
        Counts actual lines from source files to ensure sum of parts = total.
        Format: {'Section': (Source_LineCount, Generated_LineCount)}
        """
        def count_section_lines(file_path: str) -> dict:
            """Count lines for each top-level YAML section in file."""
            if not os.path.exists(file_path):
                return {}
            
            section_lines = {}
            current_section = None
            section_start = 0
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, start=1):
                stripped = line.lstrip()
                
                # Skip empty lines and comments
                if not stripped or stripped.startswith('#'):
                    continue
                
                # Detect top-level keys (no indentation before key)
                if line[0] not in (' ', '\t', '-') and ':' in line:
                    # Save previous section
                    if current_section:
                        section_lines[current_section] = i - section_start
                    
                    # Start new section
                    current_section = line.split(':')[0].strip()
                    section_start = i
            
            # Save last section
            if current_section:
                section_lines[current_section] = len(lines) - section_start + 1
            
            return section_lines
        
        source_sections = count_section_lines(self.gold_path)
        gen_sections = count_section_lines(self.gen_path)
        
        # Get union of all sections from both files
        all_sections = set(source_sections.keys()) | set(gen_sections.keys())
        
        # Standard OAS sections in display order
        ordered_sections = ['openapi', 'info', 'servers', 'paths', 'components', 
                           'security', 'tags', 'externalDocs']
        
        metrics = {}
        for section in ordered_sections:
            if section in all_sections:
                source_count = source_sections.get(section, 0)
                gen_count = gen_sections.get(section, 0)
                metrics[section.capitalize()] = (source_count, gen_count)
        
        # Add any other sections found
        for section in sorted(all_sections):
            if section not in ordered_sections:
                source_count = source_sections.get(section, 0)
                gen_count = gen_sections.get(section, 0)
                metrics[section.capitalize()] = (source_count, gen_count)
        
        return metrics
    
    def get_detailed_structure_breakdown(self) -> dict:
        """
        Returns detailed breakdown for Components and Paths sections showing where lines are lost.
        """
        import yaml
        breakdown = {}
        
        # Components breakdown by subsection
        g_comps = self.gold_oas.get('components', {})
        t_comps = self.gen_oas.get('components', {})
        
        comp_details = {}
        for key in ['schemas', 'parameters', 'responses', 'headers', 'requestBodies', 'securitySchemes']:
            g_section = g_comps.get(key, {})
            t_section = t_comps.get(key, {})
            
            def count_yaml_lines(obj):
                if not obj:
                    return 0
                return len(yaml.dump(obj, default_flow_style=False, sort_keys=False).strip().split('\n'))
            
            g_lines = count_yaml_lines(g_section)
            t_lines = count_yaml_lines(t_section)
            
            if g_lines > 0 or t_lines > 0:
                comp_details[key] = (g_lines, t_lines, t_lines - g_lines)
        
        breakdown['components'] = comp_details
        
        # Paths breakdown - find paths with biggest discrepancies
        g_paths = self.gold_oas.get('paths', {})
        t_paths = self.gen_oas.get('paths', {})
        
        path_details = []
        for path_name in set(list(g_paths.keys()) + list(t_paths.keys())):
            g_path_obj = g_paths.get(path_name, {})
            t_path_obj = t_paths.get(path_name, {})
            
            def count_yaml_lines(obj):
                if not obj:
                    return 0
                return len(yaml.dump(obj, default_flow_style=False, sort_keys=False).strip().split('\n'))
            
            g_lines = count_yaml_lines(g_path_obj)
            t_lines = count_yaml_lines(t_path_obj)
            delta = t_lines - g_lines
            
            if delta != 0:
                path_details.append((path_name, g_lines, t_lines, delta))
        
        # Sort by absolute delta (biggest losses first)
        path_details.sort(key=lambda x: abs(x[3]), reverse=True)
        breakdown['paths'] = path_details[:10]  # Top 10 discrepancies
        
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

    def _count_operations(self, paths: dict) -> int:
        count = 0
        valid_methods = {'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'}
        for path_item in paths.values():
            for key in path_item:
                if key.lower() in valid_methods:
                    count += 1
        return count
