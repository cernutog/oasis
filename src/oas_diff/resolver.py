import copy
from typing import Any, Dict, List, Set, Optional

class OASResolver:
    """
    Recursively resolves $ref references in an OpenAPI Specification,
    producing a fully flattened structure for deep semantic comparison.
    Handles cyclic references safely.
    """
    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.components = spec.get('components', {})
        # Global cache to reuse resolved components and optimize speed
        self._resolved_cache: Dict[str, Any] = {}

    def resolve(self) -> Dict[str, Any]:
        """
        Resolves the entire specification (primarily paths).
        Returns a DEEP COPY of paths with all internal $refs expanded.
        """
        paths = self.spec.get('paths', {})
        resolved_paths = {}
        
        for path, path_item in paths.items():
            # Use path-based tracking to catch cycles
            resolved_paths[path] = self._resolve_node(path_item, set())
            
        return resolved_paths

    def _resolve_node(self, node: Any, ancestors: Set[str]) -> Any:
        """
        Recursively traverses and resolves nodes.
        'ancestors' tracks the current path of $ref keys to detect cycles.
        """
        # 1. Base Cases
        if isinstance(node, list):
            return [self._resolve_node(item, ancestors) for item in node]
        if not isinstance(node, dict):
            return node

        # 2. Handle $ref
        if '$ref' in node and isinstance(node['$ref'], str):
            ref_path = node['$ref']
            
            # Simple local reference resolving (e.g. #/components/schemas/Foo)
            if ref_path.startswith('#/'):
                # Cycle Detection
                if ref_path in ancestors:
                    # Return a placeholder to break the cycle
                    return {
                        "type": "object", 
                        "description": f"[Circular Reference to {ref_path.split('/')[-1]}]"
                    }

                # Check Cache
                if ref_path in self._resolved_cache:
                    return copy.deepcopy(self._resolved_cache[ref_path])

                # Resolve Reference
                target = self._get_ref_target(ref_path)
                if target is not None:
                    # Update ancestors for recursive call
                    new_ancestors = ancestors | {ref_path}
                    # Resolve the target itself (target could have nested refs)
                    resolved_target = self._resolve_node(target, new_ancestors)
                    
                    # Merge any sibling keys (like description overrides in OAS 3.1)
                    # Sibling keys take precedence over the resolved target
                    merged = copy.deepcopy(resolved_target) if isinstance(resolved_target, dict) else resolved_target
                    if isinstance(merged, dict):
                        for k, v in node.items():
                            if k != '$ref':
                                merged[k] = self._resolve_node(v, ancestors) # Use original ancestors here
                                
                    self._resolved_cache[ref_path] = merged
                    return copy.deepcopy(merged)

        # 3. Regular Dictionary (No $ref or non-string $ref)
        resolved_dict = {}
        for k, v in node.items():
            resolved_dict[k] = self._resolve_node(v, ancestors)
            
        return resolved_dict

    def _get_ref_target(self, ref_path: str) -> Optional[Any]:
        """Retrieves the target of a local JSON pointer (e.g. #/components/schemas/User)"""
        parts = ref_path.split('/')
        if parts[0] != '#':
            return None # Only local refs supported for now
            
        current = self.spec
        try:
            for part in parts[1:]:
                # URL decoding for JSON pointer (e.g. ~1 for /, ~0 for ~)
                key = part.replace('~1', '/').replace('~0', '~')
                if isinstance(current, dict) and key in current:
                    current = current[key]
                elif isinstance(current, list) and key.isdigit():
                    current = current[int(key)]
                else:
                    return None
            return current
        except (IndexError, TypeError, ValueError):
            return None

def resolve_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to quickly resolve a spec and return the flattened paths."""
    resolver = OASResolver(spec)
    return resolver.resolve()
