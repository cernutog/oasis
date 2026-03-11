import yaml
from pathlib import Path

OAS_PATH = Path(r"C:\EBA Clearing\APIs\Generated OAS\CGS API Participants\generated_oas_3.1.yaml")


def _deref(doc, schema):
    # minimal $ref resolver for internal refs
    while isinstance(schema, dict) and "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/" ):
            return schema
        parts = ref[2:].split("/")
        cur = doc
        for p in parts:
            cur = cur.get(p)
            if cur is None:
                return schema
        schema = cur
    return schema


def main():
    if not OAS_PATH.exists():
        print(f"OAS not found: {OAS_PATH}")
        return

    doc = yaml.safe_load(OAS_PATH.read_text(encoding="utf-8"))

    schemas = ((doc or {}).get("components") or {}).get("schemas") or {}
    req = schemas.get("RevokeLcrRequest")
    if not req:
        print("Schema RevokeLcrRequest not found in components.schemas")
        return

    req = _deref(doc, req)
    print("RevokeLcrRequest keys:", list(req.keys()))
    props = req.get("properties") or {}
    print("RevokeLcrRequest.required:", req.get("required"))
    print("RevokeLcrRequest.properties:", list(props.keys()))

    sc = props.get("searchCriteria")
    if not sc:
        print("No searchCriteria property in RevokeLcrRequest")
        return

    sc = _deref(doc, sc)
    print("\nsearchCriteria schema keys:", list(sc.keys()) if isinstance(sc, dict) else type(sc))
    print("searchCriteria.required:", sc.get("required") if isinstance(sc, dict) else None)
    sc_props = (sc.get("properties") or {}) if isinstance(sc, dict) else {}
    print("searchCriteria.properties:", list(sc_props.keys()))

    # Check if networkFileName appears anywhere under searchCriteria
    if "networkFileName" in sc_props:
        nf = _deref(doc, sc_props["networkFileName"])
        print("\nnetworkFileName property schema:")
        print(nf)


if __name__ == "__main__":
    main()
