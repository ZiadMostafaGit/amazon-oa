# Hash aggregation of 2024 funds per project, roll up per village, then two tie-preserving max filters.
from typing import List, Optional, Any


def topFundedVillageProjects(villages: List[List[str]], projects: List[List[str]], funds: List[List[str]]) -> List[List[str]]:
    project_funding = {}
    for row in funds:
        pid, date, amount = row[0], row[1], row[2]
        if date[:4] == "2024":
            project_funding[pid] = project_funding.get(pid, 0) + int(amount)

    village_name = {row[0]: row[1] for row in villages}

    village_total = {}
    for pid, vid, _pname in projects:
        village_total[vid] = village_total.get(vid, 0) + project_funding.get(pid, 0)

    if not village_total:
        return []

    best_village = max(village_total.values())
    top_villages = {vid for vid, total in village_total.items() if total == best_village}

    village_best_project = {}
    for pid, vid, _pname in projects:
        if vid in top_villages:
            amt = project_funding.get(pid, 0)
            if vid not in village_best_project or amt > village_best_project[vid]:
                village_best_project[vid] = amt

    rows = []
    for pid, vid, pname in projects:
        if vid in top_villages and project_funding.get(pid, 0) == village_best_project[vid]:
            rows.append((village_name.get(vid, ""), pname, vid, pid, project_funding.get(pid, 0)))

    rows.sort(key=lambda r: (r[0], r[1], r[2], r[3]))
    return [[vname, pname, str(amount)] for vname, pname, _vid, _pid, amount in rows]
