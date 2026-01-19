"""
SWIFT Customizer for OAS Generation.

Contains functions to apply SWIFT-specific customizations to OpenAPI specifications.
"""

import copy


def apply_swift_customization(oas: dict, source_filename: str = None) -> None:
    """
    Applies SWIFT-specific customizations (Hardcoded as per exception).
    
    :param oas: The OAS dictionary to modify in-place.
    :param source_filename: Optional filename of the base OAS file to reference in description.
    """
    # 0. Custom Extension for SWIFT (Replaces 'Based on' in description)
    if "info" not in oas:
        oas["info"] = {}
    
    oas["info"]["x-info-customization"] = "SWIFT"
    
    # If source_filename was passed, we might want to log it or ignore it based on request.
    # User specifically asked to REMOVE "Based on <filename>".

    # 1. SERVERS
    oas["servers"] = [
        {
            "url": "https://api.swiftnet.sipn.swift.com/ebacl-fpad/v1",
            "description": "Live environment",
        },
        {
            "url": "https://api-test.swiftnet.sipn.swift.com/ebacl-fpad-pilot/v1",
            "description": "Test environment",
        },
    ]

    # 2. GLOBAL SECURITY
    oas["security"] = [{"oauthBearerToken": []}]

    # 3. COMPONENTS
    if "components" not in oas:
        oas["components"] = {}
    comps = oas["components"]

    # 3.1 Security Schemes
    if "securitySchemes" not in comps:
        comps["securitySchemes"] = {}
    comps["securitySchemes"]["oauthBearerToken"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "opaque OAuth 2.0",
        "description": "The access token obtained as a result of OAuth 2.0 flows. SWIFT supports two OAuth grant types depending on the API service.\n* JWT-Bearer grant type [RFC 7523](https://tools.ietf.org/html/rfc7523)\n* Password grant type\n\nThis API uses JWT-Bearer grant type.\n\nPlease visit [SWIFT OAuth Token API](https://developer.swift.com/swift-oauth-token-api) page for more information and examples on how to generate an OAuth token.\n\nIn this declaration only the basic security element to transport the bearer token of an OAuth2 process is declared.\n",
    }

    # 3.2 Parameters (ivUserKey, ivUserBic)
    if "parameters" not in comps:
        comps["parameters"] = {}

    # Ensure proper order - ivUserKey and ivUserBic MUST be first
    new_params = {}

    specific_params = {
        "ivUserKey": {
            "name": "ivUserKey",
            "in": "header",
            "description": "The subscription key of a Participant. cn=<SSO+BIC+UserId+T>,o=BIC8,o=swift. SSO is a fixed string, last char is for environment (P for production and T for test) eg SSOUNCRITMMAPI12345P, o=uncritmm,o=swift",
            "required": True,
            "schema": {
                "type": "string",
                "description": "The subscription key of a Participant. cn=<SSO+BIC+UserId+T>,o=BIC8,o=swift. SSO is a fixed string, last char is for environment (P for production and T for test) eg SSOUNCRITMMAPI12345P, o=uncritmm,o=swift",
                "example": "cn=SSOUNCRITMMAPI12345P,o=uncritmm,o=swift",
            },
        },
        "ivUserBic": {
            "name": "ivUserBic",
            "in": "header",
            "description": "BIC of the user.",
            "required": True,
            "schema": {
                "type": "string",
                "description": "BIC of the user.",
                "example": "UNCRITMM",
                "pattern": "^[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}$",
            },
        },
    }

    new_params.update(specific_params)

    # Add existing params (avoiding duplicates)
    for k, v in comps["parameters"].items():
        if k not in new_params:
            new_params[k] = v

    comps["parameters"] = new_params

    # 3.3 Headers (X-Request-ID)
    if "headers" not in comps:
        comps["headers"] = {}
    comps["headers"]["X-Request-ID"] = {
        "description": "Specify an unique end to end tracking request ID. The element will be populated by the SWIFT API gateway",
        "schema": {"type": "string"},
    }

    # 3.4 Schemas (Errors, ErrorMessage)
    if "schemas" not in comps:
        comps["schemas"] = {}

    comps["schemas"]["Errors"] = {
        "description": "Container to return multiple ErrorMessage object. Collection of error can be useful when API needs to return multiple errors, for example validation errors. When the response code conveys application-specific functional semantics and consumer can parse machine-readable error code, this block can be useful. The error response must contain at least one error object.",
        "type": "array",
        "items": {"$ref": "#/components/schemas/ErrorMessage"},
    }

    comps["schemas"]["ErrorMessage"] = {
        "description": "Custom error schema to support detailed error message.",
        "type": "object",
        "additionalProperties": False,
        "required": ["code", "severity", "text"],
        "properties": {
            "severity": {
                "description": "Specifies the severity of the error.",
                "type": "string",
                "enum": ["Fatal", "Transient", "Logic"],
            },
            "code": {
                "description": "Specifies the custom error code as defined by the service provider.",
                "type": "string",
                "minLength": 3,
                "maxLength": 70,
            },
            "text": {
                "description": "Specifies the detail error message identifying the cause of the error.",
                "type": "string",
                "minLength": 1,
                "maxLength": 255,
            },
            "user_message": {
                "description": "A human-readable text describing the error.",
                "type": "string",
                "minLength": 1,
                "maxLength": 255,
            },
            "more_info": {
                "description": "Specifies an URL to find more information about the error.",
                "type": "string",
                "format": "uri",
            },
        },
    }

    # 4. COMPONENTS MODIFICATIONS (Responses)
    # Add Header X-Request-ID to ALL Response Components
    if "responses" in comps:
        for r_name, r_obj in comps["responses"].items():
            if "headers" not in r_obj:
                r_obj["headers"] = {}
            r_obj["headers"]["X-Request-ID"] = {
                "$ref": "#/components/headers/X-Request-ID"
            }

    # 5. PATHS MODIFICATIONS
    if "paths" in oas:
        for path_url, methods in oas["paths"].items():
            for method, op in methods.items():
                if method.startswith("x-") or not isinstance(op, dict):
                    continue

                # 5.1 Inject Parameters
                if "parameters" not in op:
                    op["parameters"] = []

                # Ensure ivUserKey/ivUserBic are at the top
                new_refs = [
                    {"$ref": "#/components/parameters/ivUserKey"},
                    {"$ref": "#/components/parameters/ivUserBic"},
                ]
                existing_params = [p for p in op["parameters"] if p not in new_refs]
                op["parameters"] = new_refs + existing_params

                if "responses" in op:
                    for code, resp in op["responses"].items():

                        # 5.2 Polymorphic 400
                        if str(code) == "400" and "$ref" in resp:
                            ref_path = resp["$ref"]
                            ref_name = ref_path.split("/")[-1]
                            if (
                                "responses" in comps
                                and ref_name in comps["responses"]
                            ):
                                resp = copy.deepcopy(comps["responses"][ref_name])
                                op["responses"][code] = resp

                        if str(code) == "400":
                            if (
                                "content" in resp
                                and "application/json" in resp["content"]
                            ):
                                resp["content"]["application/json"]["schema"] = {
                                    "oneOf": [
                                        {"$ref": "#/components/schemas/ErrorResponse"},
                                        {"$ref": "#/components/schemas/Errors"},
                                    ]
                                }
                                # Remove examples from 400 responses (SWIFT requirement)
                                if "example" in resp["content"]["application/json"]:
                                    del resp["content"]["application/json"]["example"]
                                if "examples" in resp["content"]["application/json"]:
                                    del resp["content"]["application/json"]["examples"]

                        # 5.3 Inject Headers to Responses (X-Request-ID)
                        if "$ref" not in resp:
                            if "headers" not in resp:
                                resp["headers"] = {}
                            resp["headers"]["X-Request-ID"] = {
                                "$ref": "#/components/headers/X-Request-ID"
                            }

    # 6. CLEANUP (Remove x-sandbox extensions)
    clean_sandbox_extensions(oas)


def clean_sandbox_extensions(d):
    """
    Recursively removes x-sandbox-* extensions from OAS dictionary.
    """
    if isinstance(d, dict):
        keys = list(d.keys())
        for k in keys:
            if k == "__RAW_EXTENSIONS__" and isinstance(d[k], str):
                lines = d[k].split("\n")
                filtered_lines = []
                skip_level = -1

                for line in lines:
                    stripped = line.lstrip()
                    if not stripped:
                        if skip_level == -1:
                            filtered_lines.append(line)
                        continue

                    current_indent = len(line) - len(stripped)

                    if skip_level != -1 and current_indent > skip_level:
                        continue

                    skip_level = -1

                    if stripped.startswith("x-sandbox"):
                        skip_level = current_indent
                        continue

                    filtered_lines.append(line)

                new_text = "\n".join(filtered_lines)

                if not new_text.strip():
                    del d[k]
                else:
                    d[k] = new_text

            elif k.startswith("x-sandbox"):
                del d[k]
            else:
                clean_sandbox_extensions(d[k])
    elif isinstance(d, list):
        for item in d:
            clean_sandbox_extensions(item)
