
import hashlib
import re
from typing import Dict, List, Optional, Tuple, Set
from .v3_models import (
    SchemaGraph,
    EnrichedNode,
    EnrichedOperation,
    NodeClass
)

class NameRegistry:
    def __init__(self):
        # structural_hash -> final_name
        self.hash_to_name: Dict[str, str] = {}
        # base_name -> count
        self.base_counts: Dict[str, int] = {}
        # final_name -> EnrichedNode
        self.definitions: Dict[str, EnrichedNode] = {}
        # lower_orig_name -> final_name (for anchor mapping)
        self.literal_map: Dict[str, str] = {}

    def register_definition(self, base_name: str, structural_hash: Optional[str], node: EnrichedNode, force_pascal: bool = True) -> str:
        if structural_hash and structural_hash in self.hash_to_name:
            return self.hash_to_name[structural_hash]
        
        # Preserve original name as much as possible for parity
        # BUT: Enforce PascalCase for everything except Request/Response roots
        # This fixes 'alerts' (camel) appearing as a global schema, and 'senderBIC' -> 'SenderBIC'
        should_force_pascal = force_pascal
        if not force_pascal:
            if not (base_name.endswith("Request") or base_name.endswith("Response")):
                should_force_pascal = True

        final_base = self._to_pascal_case(base_name) if should_force_pascal else base_name
        
        if final_base not in self.base_counts:
            self.base_counts[final_base] = 0
            final_name = final_base
        else:
            self.base_counts[final_base] += 1
            final_name = f"{final_base}{self.base_counts[final_base]}"
            
        if structural_hash:
            self.hash_to_name[structural_hash] = final_name
        
        target_type = node.type_literal
        if not target_type or target_type.lower() == "nan":
             target_type = "object" if node.properties else "string"
        elif target_type.lower() == final_base.lower() or target_type.lower() == base_name.lower():
             # Normalize self-reference to object to prevent hash divergence
             target_type = "object" if node.properties else "string"
             
        canonical = EnrichedNode(
            name=final_name,
            node_class=NodeClass.DOMAIN_CONCEPT,
            type_literal=target_type,
            is_collection=False,
            description=node.description,
            properties=node.properties,
            items_type_literal=node.items_type_literal,
            format=node.format,
            min_val=node.min_val,
            max_val=node.max_val,
            pattern_eba=node.pattern_eba,
            regex=node.regex,
            allowed_values=node.allowed_values,
            example=node.example,
            custom_extensions=node.custom_extensions,
            lineage=node.lineage
        )
        self.definitions[final_name] = canonical
        return final_name

    def _to_pascal_case(self, s: str) -> str:
        if not s: return s
        return s[0].upper() + s[1:]

class V3Harmonizer:
    def __init__(self, graph: SchemaGraph):
        self.graph = graph
        self.registry = NameRegistry()

    def harmonize(self):
        # Phase 1: Explicit Domain Concepts
        for node in list(self.graph.global_schemas):
            # FILTER: Skip "Empty Objects" (shells defined in Data Type without properties)
            # This allows the FULL definition found in Operations (Phase 2) to claim the name.
            # We keep atomic types (string, integer) or objects with properties.
            filtered = False
            t_lit = node.type_literal.lower()
            
            # Check for constraints (if present, likely a valid simple type like DateTime)
            has_constraints = any([node.format, node.pattern_eba, node.regex, node.allowed_values, node.min_val, node.max_val])
            
            if not node.properties and not has_constraints:
                # If no props and no constraints, strict check on type
                if t_lit in ["object", "string", "nan"]:
                    filtered = True
                elif t_lit == "array":
                     # Skip arrays without specific items
                     i_lit = node.items_type_literal
                     if not i_lit or i_lit.lower() in ["object", "nan", "string", ""]:
                         filtered = True
            
            if filtered:
                continue

            # We computes hash so subsequent identical structures collapse onto this name
            # We computes hash so subsequent identical structures collapse onto this name
            structural_hash = None
            if node.properties or has_constraints:
                structural_hash = self._calculate_deep_hash(node)
                
            final_name = self.registry.register_definition(node.name, structural_hash=structural_hash, node=node, force_pascal=True)
            self.registry.literal_map[node.name.lower()] = final_name

        # Phase 2: Operations
        for op in self.graph.operations.values():
            if op.request: self._process_recursive(op.request, is_root=True)
            for resp in op.responses.values():
                self._process_recursive(resp, is_root=True)

        self.graph.global_schemas = list(self.registry.definitions.values())

    def _process_recursive(self, node: EnrichedNode, is_root: bool):
        if not is_root:
            orig_type_lit = node.type_literal.lower()
            if orig_type_lit in self.registry.literal_map:
                node.type_literal = self.registry.literal_map[orig_type_lit]
            node.name = self._to_camel_case(node.name)
        else:
             # Preserve exact root name for parity
             pass

        for p in node.properties:
            self._process_recursive(p, is_root=False)

            # UNIQUE IDs to prevent over-unification (but unify consistent primitives)
            # Calculate hash if properties OR constraints exist
            has_constraints = any([node.format, node.pattern_eba, node.regex, node.allowed_values, node.min_val, node.max_val])
            
            reg_hash = None
            if node.properties or has_constraints:
                 f_hash = self._calculate_deep_hash(node)
                 reg_hash = f_hash if not is_root else None

            # PROMOTED nested objects get PascalCase suffix, Roots keep original
            final_name = self.registry.register_definition(node.name, structural_hash=reg_hash, node=node, force_pascal=not is_root)
            
            if not is_root:
                if node.is_collection:
                    node.type_literal = "array"
                    node.items_type_literal = final_name
                else:
                    node.type_literal = final_name
            else:
                node.type_literal = final_name

    def _calculate_deep_hash(self, node: EnrichedNode) -> str:
        # Normalize type for hashing (handle self-ref)
        t_lit = node.type_literal or ""
        if t_lit.lower() == node.name.lower():
            t_lit = "object" if node.properties else "string"

        # Include Type and Constraints in Hash
        constraints = "|".join([
            str(t_lit),
            str(node.format or ""),
            str(node.regex or ""),
            str(node.pattern_eba or ""),
            str(node.min_val or ""),
            str(node.max_val or ""),
            str(node.allowed_values or "")
        ])

        props_data = []
        for p in node.properties:
            p_name = self._to_camel_case(p.name)
            p_type = p.type_literal
            p_mandatory = "M" if p.mandatory else "O"
            p_constraints = "|".join([str(p.format or ""), str(p.regex or ""), str(p.allowed_values or "")])
            props_data.append(f"{p_name}|{p_type}|{p_mandatory}|[{p_constraints}]")
        
        props_data.sort()
        content = f"HEAD[{constraints}]||BODY[{'||'.join(props_data)}]"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _to_camel_case(self, s: str) -> str:
        if not s: return s
        # preserve acronyms like BIC
        if len(s) > 1 and s[0].isupper() and s[1].islower():
            return s[0].lower() + s[1:]
        return s
