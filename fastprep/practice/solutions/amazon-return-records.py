# Direct simulation with a dict of credentials and a set of active sessions.
from typing import List


def returnRecords(attempts: List[str]) -> List[str]:
    passwords = {}
    logged_in = set()
    out = []
    for request in attempts:
        parts = request.split()
        action = parts[0]
        if action == "register":
            user, pwd = parts[1], parts[2]
            if user in passwords:
                out.append("Register Unsuccessfully")
            else:
                passwords[user] = pwd
                out.append("Registered Successfully")
        elif action == "login":
            user, pwd = parts[1], parts[2]
            if user in passwords and passwords[user] == pwd and user not in logged_in:
                logged_in.add(user)
                out.append("Logged In Successfully")
            else:
                out.append("Login Unsuccessfully")
        else:
            user = parts[1]
            if user in logged_in:
                logged_in.discard(user)
                out.append("Logged Out Successfully")
            else:
                out.append("Logout Unsuccessfully")
    return out
