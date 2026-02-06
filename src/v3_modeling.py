
from typing import List, Dict, Optional
from .v3_models import (
    LegacyIntermediateRepresentation,
    SchemaGraph,
    RawNode,
    EnrichedNode,
    EnrichedOperation,
    NodeClass
)

class V3Modeler:
    def __init__(self, ir: LegacyIntermediateRepresentation):
        self.ir = ir
        self.graph = SchemaGraph()

    def build_graph(self) -> SchemaGraph:
        """Transforms RAW IR into a semantic graph with virtual root hoisting."""
        # 1. Process Operations
        for op_id, op_node in self.ir.operations.items():
            en_op = EnrichedOperation(operation_id=op_id)
            
            # Request Hoisting (from Body, Header, Path)
            if "Body" in op_node.sheets:
                en_op.request = self._hoist_virtual_root(
                    f"{op_id}Request", 
                    op_node.sheets["Body"],
                    NodeClass.OPERATION_ROOT
                )
            
            # Response Hoisting
            for sheet_name, nodes in op_node.sheets.items():
                if sheet_name.isdigit(): # e.g. "200", "404"
                    en_op.responses[sheet_name] = self._hoist_virtual_root(
                        f"{op_id}Response",
                        nodes,
                        NodeClass.OPERATION_ROOT
                    )
            
            self.graph.operations[op_id] = en_op
            
        # 2. Process Global Domain Concepts (Data Type sheets)
        for name, raw in self.ir.domain_concepts.items():
            en = self._transform_node(raw)
            en.node_class = NodeClass.DOMAIN_CONCEPT
            self.graph.global_schemas.append(en)

        return self.graph

    def _hoist_virtual_root(self, name: str, raw_roots: List[RawNode], node_class: NodeClass) -> EnrichedNode:
        """Creates a virtual container for flat Excel rows."""
        root = EnrichedNode(
            name=name,
            node_class=node_class,
            type_literal="object",
            description=name
        )
        for raw in raw_roots:
            root.properties.append(self._transform_node(raw))
        return root

    def _transform_node(self, raw: RawNode) -> EnrichedNode:
        """Recursive transformation of RawNode to EnrichedNode."""
        node = EnrichedNode(
            name=raw.name,
            node_class=NodeClass.OBJECT_PROPERTY,
            type_literal=raw.type_literal,
            items_type_literal=raw.items_type_literal,
            mandatory=raw.mandatory,
            description=raw.description,
            is_collection=(raw.type_literal.lower() == "array"),
            
            # Propagation of Metadata
            format=raw.format,
            min_val=raw.min_val,
            max_val=raw.max_val,
            pattern_eba=raw.pattern_eba,
            regex=raw.regex,
            allowed_values=raw.allowed_values,
            example=raw.example,
            
            custom_extensions=raw.custom_extensions,
            lineage=raw.lineage
        )
        
        for child in raw.children:
            node.properties.append(self._transform_node(child))
            
        return node
