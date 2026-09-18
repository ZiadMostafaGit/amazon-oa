# Runs inside the sandbox. Builds a fresh in-memory SQLite database per visible
# case from `inputSchema` + `case.input`, runs the user's query, and compares
# the rows against `expectedResult` under the problem's own result contract
# (column set, row order, numeric tolerance).

def _main():
    import base64, json, sqlite3, sys

    payload = json.loads(base64.b64decode(_PAYLOAD_B64))
    query, tab, cap = payload["query"], payload["tabular"], payload["maxOutput"]
    schema = tab.get("inputSchema") or []
    contract = tab.get("resultContract") or {}
    tol = contract.get("numericTolerance") or 0
    row_order = (contract.get("rowOrder") or "exact").lower()

    def emit(obj):
        sys.stdout.write("\n#---RESULT:%s---\n" % _NONCE + json.dumps(obj, default=str))
        sys.stdout.flush()

    SQL_TYPE = {"integer": "INTEGER", "decimal": "REAL", "text": "TEXT",
                "boolean": "INTEGER", "date": "TEXT", "timestamp": "TEXT"}

    statements = [s for s in (query or "").split(";") if s.strip()]
    if not statements:
        return emit({"error": "write a SELECT statement first"})
    if len(statements) > 1:
        return emit({"error": "run one statement at a time (%d were given)" % len(statements)})

    # The contract declares each result column's type, and the bank does not
    # always honour it in its own expected values: a "decimal" column can carry
    # the string "100" while SQLite returns 100.0. Compare by the DECLARED type
    # rather than by the Python types that happen to show up.
    col_types = [c.get("type") for c in (contract.get("columns") or [])]
    NUMERIC = ("decimal", "integer", "float", "double", "numeric")

    def same(a, b, col=None):
        if a is None or b is None:
            return a is None and b is None
        declared = col_types[col] if col is not None and col < len(col_types) else None
        if declared in NUMERIC:
            try:
                return abs(float(a) - float(b)) <= (float(tol) if tol else 0)
            except (TypeError, ValueError):
                return str(a) == str(b)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
                and not isinstance(a, bool) and not isinstance(b, bool):
            return abs(float(a) - float(b)) <= (float(tol) if tol else 0)
        return str(a) == str(b)

    results = []
    for case in tab.get("visibleCases") or []:
        entry = {"id": case.get("id"), "explanation": case.get("explanation")}
        con = sqlite3.connect(":memory:")
        con.execute("PRAGMA trusted_schema=OFF")
        try:
            for table in schema:
                cols = ", ".join('"%s" %s' % (c["name"], SQL_TYPE.get(c.get("type"), "TEXT"))
                                 for c in table["columns"])
                con.execute('CREATE TABLE "%s" (%s)' % (table["name"], cols))
                rows = (case.get("input") or {}).get(table["name"]) or []
                if rows:
                    con.executemany('INSERT INTO "%s" VALUES (%s)' %
                                    (table["name"], ",".join("?" * len(table["columns"]))), rows)
            cur = con.execute(statements[0])
            got_cols = [d[0] for d in (cur.description or [])]
            got_rows = [list(r) for r in cur.fetchmany(5000)]
        except Exception as e:
            entry.update(ok=False, error="%s: %s" % (type(e).__name__, e))
            results.append(entry); con.close(); continue
        con.close()

        exp = case.get("expectedResult") or {}
        exp_cols = list(exp.get("columns") or [])
        exp_rows = [list(r) for r in (exp.get("rows") or [])]

        problems = []
        if [c.lower() for c in got_cols] != [c.lower() for c in exp_cols]:
            problems.append("columns are %s, expected %s" % (got_cols, exp_cols))
        else:
            a, b = got_rows, exp_rows
            if row_order != "exact":
                a = sorted(a, key=lambda r: json.dumps(r, default=str))
                b = sorted(b, key=lambda r: json.dumps(r, default=str))
            if len(a) != len(b):
                problems.append("%d row(s), expected %d" % (len(a), len(b)))
            else:
                for i, (ra, rb) in enumerate(zip(a, b)):
                    if not all(same(x, y, k) for k, (x, y) in enumerate(zip(ra, rb))):
                        problems.append("row %d is %s, expected %s" % (i + 1, ra, rb))
                        break

        entry.update(ok=not problems, columns=got_cols, rows=got_rows[:200],
                     expectedColumns=exp_cols, expectedRows=exp_rows[:200],
                     rowOrder=row_order,
                     error="; ".join(problems) if problems else None)
        results.append(entry)

    emit({"results": results})


_main()
