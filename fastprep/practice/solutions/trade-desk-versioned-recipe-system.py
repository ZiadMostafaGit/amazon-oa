# Command interpreter over a dict of recipes, each keeping an append-only version list.
from typing import List, Optional, Any


def processRecipeCommands(commands: List[str]) -> List[str]:
    recipes = {}  # recipe_id -> {"user": str, "versions": [(name, content)], "deleted": bool}
    out = []

    def fmt_get(rid, rec, idx):
        name, content = rec["versions"][idx]
        return "%s|%s|v%d|%s|%s" % (rid, rec["user"], idx + 1, name, content)

    def parse_version(rec, token):
        try:
            v = int(token)
        except ValueError:
            return None
        if v < 1 or v > len(rec["versions"]):
            return None
        return v

    def listing(pairs):
        if not pairs:
            return "EMPTY"
        return ";".join("%s:v%d:%s" % (rid, len(rec["versions"]), rec["versions"][-1][0])
                        for rid, rec in pairs)

    for raw in commands:
        parts = raw.split("|")
        op = parts[0] if parts else ""

        if op == "ADD" and len(parts) == 5:
            _, rid, uid, name, content = parts
            if rid in recipes:
                out.append("ERROR")
            else:
                recipes[rid] = {"user": uid, "versions": [(name, content)], "deleted": False}
                out.append("OK v1")

        elif op == "GET" and len(parts) in (2, 3):
            rid = parts[1]
            rec = recipes.get(rid)
            if rec is None:
                out.append("NOT_FOUND")
            elif len(parts) == 2:
                out.append("NOT_FOUND" if rec["deleted"] else fmt_get(rid, rec, len(rec["versions"]) - 1))
            else:
                v = parse_version(rec, parts[2])
                out.append("NOT_FOUND" if v is None else fmt_get(rid, rec, v - 1))

        elif op == "UPDATE" and len(parts) == 5:
            _, rid, uid, name, content = parts
            rec = recipes.get(rid)
            if rec is None or rec["deleted"]:
                out.append("NOT_FOUND")
            elif rec["user"] != uid:
                out.append("FORBIDDEN")
            else:
                if rec["versions"][-1] != (name, content):
                    rec["versions"].append((name, content))
                out.append("OK v%d" % len(rec["versions"]))

        elif op == "DELETE" and len(parts) == 3:
            _, rid, uid = parts
            rec = recipes.get(rid)
            if rec is None or rec["deleted"]:
                out.append("NOT_FOUND")
            elif rec["user"] != uid:
                out.append("FORBIDDEN")
            else:
                rec["deleted"] = True
                out.append("OK")

        elif op == "ROLLBACK" and len(parts) == 4:
            _, rid, uid, token = parts
            rec = recipes.get(rid)
            if rec is None or rec["deleted"]:
                out.append("NOT_FOUND")
            elif rec["user"] != uid:
                out.append("FORBIDDEN")
            else:
                v = parse_version(rec, token)
                if v is None:
                    out.append("NOT_FOUND")
                else:
                    rec["versions"].append(rec["versions"][v - 1])
                    out.append("OK v%d" % len(rec["versions"]))

        elif op == "HISTORY" and len(parts) == 2:
            rec = recipes.get(parts[1])
            if rec is None:
                out.append("NOT_FOUND")
            else:
                out.append(";".join("v%d:%s" % (i + 1, nv[0])
                                    for i, nv in enumerate(rec["versions"])))

        elif op == "LIST" and len(parts) in (1, 2):
            items = [(rid, rec) for rid, rec in recipes.items() if not rec["deleted"]]
            if len(parts) == 2:
                items = [p for p in items if p[1]["user"] == parts[1]]
            items.sort(key=lambda p: p[0])
            out.append(listing(items))

        elif op == "SEARCH" and len(parts) == 2:
            key = parts[1].lower()
            items = []
            for rid, rec in recipes.items():
                if rec["deleted"]:
                    continue
                name, content = rec["versions"][-1]
                if key in name.lower() or key in content.lower():
                    items.append((rid, rec))
            items.sort(key=lambda p: p[0])
            out.append(listing(items))

        else:
            out.append("ERROR")

    return out
