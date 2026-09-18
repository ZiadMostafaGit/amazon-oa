# Recursive descent over parsed JSON: compare key sets, then match leaf descriptors.
import json


def _match(schema, doc) -> bool:
    if isinstance(schema, str):
        if schema == "string":
            return isinstance(doc, str)
        if schema == "number":
            return isinstance(doc, int) and not isinstance(doc, bool)
        return False
    if not isinstance(schema, dict) or not isinstance(doc, dict):
        return False
    if schema.keys() != doc.keys():
        return False
    for key, sub in schema.items():
        if not _match(sub, doc[key]):
            return False
    return True


def validateNestedObjectSchema(schema: str, document: str) -> bool:
    try:
        s = json.loads(schema)
        d = json.loads(document)
    except ValueError:
        return False
    return _match(s, d)
