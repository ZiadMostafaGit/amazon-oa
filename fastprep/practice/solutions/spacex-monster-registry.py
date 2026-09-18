# Parse the CSV rows, match type/weakness sets, and DFS the evolution graph in ID order.
from typing import List
import csv


def buildMonsterRegistry(databaseRows: List[str], monsterName: str) -> str:
    reader = csv.reader(databaseRows)
    rows = [row for row in reader if row]
    header = rows[0]
    index = {name.strip(): position for position, name in enumerate(header)}
    id_col = index["ID"]
    name_col = index["Name"]
    types_col = index["Types"]
    weak_col = index["Weaknesses"]
    evo_col = index["Evolution"]

    def split_field(text: str) -> List[str]:
        return [part.strip() for part in text.split(",") if part.strip()]

    monsters = {}
    order = []
    for row in rows[1:]:
        mid = row[id_col].strip()
        monsters[mid] = {
            "id": mid,
            "name": row[name_col].strip(),
            "types": split_field(row[types_col]),
            "weaknesses": split_field(row[weak_col]),
            "evolution": split_field(row[evo_col]),
        }
        order.append(mid)

    order.sort(key=lambda mid: int(mid))

    target = None
    wanted = monsterName.strip().lower()
    for mid in order:
        if monsters[mid]["name"].lower() == wanted:
            target = monsters[mid]
            break

    my_types = set(target["types"])
    my_weaknesses = set(target["weaknesses"])

    strong_against = []
    weak_against = []
    for mid in order:
        other = monsters[mid]
        if my_types & set(other["weaknesses"]):
            strong_against.append(other["name"])
        if my_weaknesses & set(other["types"]):
            weak_against.append(other["name"])

    paths = []

    def walk(mid: str, trail: List[str]) -> None:
        trail.append(monsters[mid]["name"])
        children = sorted(monsters[mid]["evolution"], key=lambda c: int(c))
        if not children:
            paths.append(" > ".join(trail))
        else:
            for child in children:
                walk(child, trail)
        trail.pop()

    walk(target["id"], [])

    lines = ["ID:", "    " + target["id"]]
    lines.append("Strong against:")
    lines.extend("    " + name for name in (strong_against or ["None"]))
    lines.append("Weak against:")
    lines.extend("    " + name for name in (weak_against or ["None"]))
    lines.append("Evolution:")
    lines.extend("    " + path for path in paths)
    return "\n".join(lines) + "\n"
