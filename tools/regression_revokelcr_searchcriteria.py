import yaml
from pathlib import Path


def _deref(doc, schema):
    while isinstance(schema, dict) and "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            return schema
        cur = doc
        for part in ref[2:].split("/"):
            cur = cur.get(part)
            if cur is None:
                return schema
        schema = cur
    return schema


def _get_path_item(doc):
    return doc.get("paths", {}).get("/revokeLcr/{senderBIC}", {}).get("put", {})


def main():
    oas_path = Path(r"C:\EBA Clearing\APIs\Generated OAS\CGS API Participants\generated_oas_3.1.yaml")
    if not oas_path.exists():
        print(f"OAS not found: {oas_path}")
        raise SystemExit(2)

    doc = yaml.safe_load(oas_path.read_text(encoding="utf-8"))

    put = _get_path_item(doc)
    if not put:
        print("/revokeLcr/{senderBIC} put not found")
        raise SystemExit(2)

    rb = put.get("requestBody", {}).get("content", {}).get("application/json", {})
    schema = _deref(doc, rb.get("schema", {}))
    props = schema.get("properties", {}) if isinstance(schema, dict) else {}
    sc = _deref(doc, props.get("searchCriteria", {}))

    if not isinstance(sc, dict):
        print("searchCriteria schema not a dict")
        raise SystemExit(2)

    required = sc.get("required") or []
    if "networkFileName" in required:
        print("[FAIL] RevokeLcrRequest.searchCriteria.required contains networkFileName")
        raise SystemExit(1)

    print("[PASS] RevokeLcrRequest.searchCriteria.required does NOT contain networkFileName")


if __name__ == "__main__":
    main()
