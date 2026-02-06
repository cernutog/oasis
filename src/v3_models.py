
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

class NodeClass(Enum):
    OPERATION_ROOT = "operation_root"
    DOMAIN_CONCEPT = "domain_concept"
    OBJECT_PROPERTY = "object_property"

@dataclass
class SourceLineage:
    file: str
    sheet: str
    row: int

@dataclass
class RawNode:
    name: str
    parent_name: Optional[str]
    type_literal: str
    mandatory: bool
    description: str
    items_type_literal: Optional[str] = None
    
    # NEW: Constraint fields
    format: Optional[str] = None
    min_val: Optional[str] = None
    max_val: Optional[str] = None
    pattern_eba: Optional[str] = None
    regex: Optional[str] = None
    allowed_values: Optional[str] = None
    example: Optional[str] = None
    
    custom_extensions: Optional[str] = None
    lineage: Optional[SourceLineage] = None
    children: List['RawNode'] = field(default_factory=list)

@dataclass
class OperationNode:
    operation_id: str
    method: str
    path: str
    summary: str
    description: str
    tags: List[str]
    sheets: Dict[str, List[RawNode]] = field(default_factory=dict)

@dataclass
class LegacyIntermediateRepresentation:
    operations: Dict[str, OperationNode] = field(default_factory=dict)
    domain_concepts: Dict[str, RawNode] = field(default_factory=dict)
    info: Dict[str, str] = field(default_factory=dict)
    servers: List[str] = field(default_factory=list)

@dataclass
class EnrichedNode:
    name: str
    node_class: NodeClass
    type_literal: str
    items_type_literal: Optional[str] = None
    is_collection: bool = False
    mandatory: bool = False
    description: str = ""
    
    # NEW: Constraint fields preservation
    format: Optional[str] = None
    min_val: Optional[str] = None
    max_val: Optional[str] = None
    pattern_eba: Optional[str] = None
    regex: Optional[str] = None
    allowed_values: Optional[str] = None
    example: Optional[str] = None
    
    custom_extensions: Optional[str] = None
    lineage: Optional[SourceLineage] = None
    properties: List['EnrichedNode'] = field(default_factory=list)
    fingerprint: Optional[str] = None

@dataclass
class EnrichedOperation:
    operation_id: str
    request: Optional[EnrichedNode] = None
    responses: Dict[str, EnrichedNode] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SchemaGraph:
    operations: Dict[str, EnrichedOperation] = field(default_factory=dict)
    global_schemas: List[EnrichedNode] = field(default_factory=list)
