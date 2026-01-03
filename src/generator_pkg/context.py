"""
Generator Context for OAS Generation.

Provides a shared context object that modules can use without
tight coupling to OASGenerator class.
"""

from collections import OrderedDict


class GeneratorContext:
    """
    Shared context for OAS generation modules.
    
    Contains the OAS version and the OAS document being built.
    Modules receive this context instead of the full OASGenerator.
    """
    
    def __init__(self, version: str = "3.0.0"):
        self.version = version
        self.oas = {
            "openapi": version,
            "info": {},
            "paths": {},
            "components": {
                "parameters": {},
                "headers": {},
                "schemas": {},
                "responses": {},
                "securitySchemes": {},
            },
        }
    
    def is_oas31(self) -> bool:
        """Check if generating OAS 3.1.x"""
        return self.version.startswith("3.1")
    
    def is_oas30(self) -> bool:
        """Check if generating OAS 3.0.x"""
        return self.version.startswith("3.0")
