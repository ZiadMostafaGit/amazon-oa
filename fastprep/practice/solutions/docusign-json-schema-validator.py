# Strict JSON parse (duplicate-key aware) + grammar validation of the schema, then per-property checks.
import json
import re

_NUM_RE = re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?')
_TYPES = ("string", "number", "boolean")


class _Bad(Exception):
    pass


def _pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise _Bad("duplicate key")
        d[k] = v
    return d


def _const(_name):
    raise _Bad("bad constant")


def _parse(text):
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=_const)


def _is_str(v):
    return isinstance(v, str)


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _parse_limit(text):
    if not _is_str(text):
        raise _Bad("limit not a string")
    m = _NUM_RE.match(text)
    if not m or m.start() != 0:
        raise _Bad("bad limit")
    low = m.group(0)
    rest = text[m.end():]
    if not rest.startswith("-"):
        raise _Bad("bad limit")
    high = rest[1:]
    if not _NUM_RE.fullmatch(high):
        raise _Bad("bad limit")
    return float(low), float(high)


def _build_rules(schema):
    if not isinstance(schema, dict):
        raise _Bad("schema not an object")
    for key in schema:
        if key not in ("_type", "properties"):
            raise _Bad("unknown schema field")
    if "_type" not in schema or "properties" not in schema:
        raise _Bad("missing schema field")
    stype = schema["_type"]
    if not _is_str(stype) or stype == "":
        raise _Bad("bad schema type")
    props = schema["properties"]
    if not isinstance(props, list):
        raise _Bad("properties not an array")
    rules = {}
    for raw in props:
        if not isinstance(raw, dict):
            raise _Bad("rule not an object")
        for key in raw:
            if key not in ("name", "type", "required", "validation", "limit"):
                raise _Bad("unknown rule field")
        if "name" not in raw or "type" not in raw:
            raise _Bad("missing rule field")
        name = raw["name"]
        if not _is_str(name) or name == "":
            raise _Bad("bad rule name")
        if name in rules:
            raise _Bad("duplicate rule name")
        rtype = raw["type"]
        if not _is_str(rtype) or rtype not in _TYPES:
            raise _Bad("bad rule type")
        required = raw.get("required", False)
        if not isinstance(required, bool):
            raise _Bad("bad required flag")
        pattern = None
        limit = None
        if "validation" in raw:
            if rtype != "string":
                raise _Bad("validation on non-string")
            pat = raw["validation"]
            if not _is_str(pat):
                raise _Bad("validation not a string")
            try:
                pattern = re.compile(pat)
            except re.error:
                raise _Bad("bad regex")
        if "limit" in raw:
            if rtype != "number":
                raise _Bad("limit on non-number")
            limit = _parse_limit(raw["limit"])
        rules[name] = (rtype, required, pattern, limit)
    return stype, rules


def validateObject(schemaJson: str, objectJson: str) -> bool:
    try:
        schema = _parse(schemaJson)
        obj = _parse(objectJson)
        stype, rules = _build_rules(schema)
    except (_Bad, ValueError, RecursionError):
        return False

    if not isinstance(obj, dict):
        return False
    otype = obj.get("_type")
    if not _is_str(otype) or otype == "" or otype != stype:
        return False

    for key, value in obj.items():
        if key == "_type":
            continue
        rule = rules.get(key)
        if rule is None:
            return False
        rtype, _req, pattern, limit = rule
        if rtype == "string":
            if not _is_str(value):
                return False
            if pattern is not None and pattern.fullmatch(value) is None:
                return False
        elif rtype == "number":
            if not _is_num(value):
                return False
            if limit is not None and not (limit[0] <= float(value) <= limit[1]):
                return False
        else:
            if not isinstance(value, bool):
                return False

    for name, rule in rules.items():
        if rule[1] and name not in obj:
            return False
    return True
