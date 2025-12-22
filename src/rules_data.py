
SPECTRAL_RULES = {
    # Core OAS 3.x Rules
    "oas3-api-servers": {
        "description": "OpenAPI object should include a `servers` array.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-api-servers"
    },
    "oas3-examples-value-or-externalValue": {
        "description": "Examples must have either `value` or `externalValue` field.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-examples-value-or-externalvalue"
    },
    "oas3-operation-security-defined": {
        "description": "Operation security must reference a defined security scheme.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-operation-security-defined"
    },
    "oas3-parameter-description": {
        "description": "Parameter objects should have a `description`.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-parameter-description"
    },
    "oas3-schema": {
        "description": "Object must align with the OpenAPI 3.0 schema.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-schema"
    },
    "oas3-server-trailing-slash": {
        "description": "Server URL should not have a trailing slash.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-server-trailing-slash"
    },
    "oas3-unused-component": {
        "description": "Potentially unused component has been detected.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-unused-component"
    },
    "oas3-valid-media-example": {
        "description": "Examples must be valid against their defined schema.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-valid-media-example"
    },
    "oas3-valid-schema-example": {
        "description": "Schema examples must be valid against the schema.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#oas3-valid-schema-example"
    },
    "operation-description": {
        "description": "Operation must have a description.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#operation-description"
    },
    "operation-operationId": {
        "description": "Operation must have a unique `operationId`.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#operation-operationid"
    },
    "operation-operationId-unique": {
        "description": "Every operation must have a unique `operationId`.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#operation-operationid-unique"
    },
    "operation-parameters": {
        "description": "Operation parameters are unique and valid.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#operation-parameters"
    },
    "operation-success-response": {
        "description": "Operation must have at least one 2xx or 3xx response.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#operation-success-response"
    },
    "operation-tag-defined": {
        "description": "Operation tags must be defined in global tags.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#operation-tag-defined"
    },
    "operation-tags": {
        "description": "Operation should have tags.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#operation-tags"
    },
    "path-declarations-must-exist": {
        "description": "Path parameter declarations must exist in the path string.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#path-declarations-must-exist"
    },
    "path-keys-no-trailing-slash": {
        "description": "Path keys should not end with a slash.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#path-keys-no-trailing-slash"
    },
    "path-not-include-query": {
        "description": "Path keys should not include query parameters.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#path-not-include-query"
    },
    "path-params": {
        "description": "Path parameters must be defined and valid.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#path-params"
    },
    "typed-enum": {
        "description": "Enum values must respect the specified type.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#typed-enum"
    },
    "contact-properties": {
        "description": "Contact object should have name, url, and email.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#contact-properties"
    },
    "info-contact": {
        "description": "Info object must have a `contact` object.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#info-contact"
    },
    "info-description": {
        "description": "Info object must have a `description`.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#info-description"
    },
    "info-license": {
        "description": "Info object must have a `license` object.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#info-license"
    },
    "license-url": {
        "description": "License object should include a `url`.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#license-url"
    },
    "no-script-tags-in-markdown": {
        "description": "Markdown descriptions should not contain `<script>` tags.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#no-script-tags-in-markdown"
    },
    "openapi-tags": {
        "description": "OpenAPI object should have non-empty `tags` array.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#openapi-tags"
    },
    "openapi-tags-alphabetical": {
        "description": "Tags should be sorted alphabetically.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#openapi-tags-alphabetical"
    },
    "tag-description": {
        "description": "Tag objects should have a `description`.",
        "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules#tag-description"
    },
    # Generic / Custom fallbacks
    "no-unused-components": {
         "description": "Component is defined but never used.",
         "url": "https://docs.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules"
    }
}
