# Count position tallies per team, then sort by the tally vector descending with the team letter as tiebreak.
from typing import List, Optional, Any


def rankTeams(votes: List[str]) -> str:
    if not votes:
        return ""
    teams = list(votes[0])
    positions = len(teams)
    tally = {team: [0] * positions for team in teams}
    for vote in votes:
        for rank, team in enumerate(vote):
            tally[team][rank] += 1
    teams.sort(key=lambda team: ([-count for count in tally[team]], team))
    return "".join(teams)
