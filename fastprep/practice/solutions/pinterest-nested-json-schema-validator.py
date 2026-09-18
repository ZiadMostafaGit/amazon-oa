# Parse both strings with json, then recursively match the document against the schema node.
import json


def _match(schema, value) -> bool:
    if isinstance(schema, str):
        if schema == "string":
            return isinstance(value, str)
        if schema == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if schema == "boolean":
            return isinstance(value, bool)
        return False
    if isinstance(schema, dict):
        if "array" in schema:
            if not isinstance(value, list):
                return False
            child = schema["array"]
            return all(_match(child, item) for item in value)
        if "object" in schema:
            if not isinstance(value, dict):
                return False
            fields = schema["object"]
            if set(fields.keys()) != set(value.keys()):
                return False
            return all(_match(fields[k], value[k]) for k in fields)
    return False


def validateNestedJsonSchema(schema: str, document: str) -> bool:
    return _match(json.loads(schema), json.loads(document))
