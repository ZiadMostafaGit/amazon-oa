def countTargetParents(preorder: str, target: int) -> int:
    tokens = [t.strip() for t in preorder.split(",")]
    pos = 0
    count = 0
    # Iterative preorder rebuild: frame = [value, left, right, stage]
    # Returns value or None per subtree; we only need direct-child values.
    stack = []
    result = None

    def read():
        nonlocal pos
        t = tokens[pos]
        pos += 1
        return None if t == "#" else int(t)

    v = read()
    if v is None:
        return 0
    stack.append([v, None, None, 0])
    while stack:
        top = stack[-1]
        if top[3] == 2:
            stack.pop()
            if top[1] is not None and top[2] is not None and top[0] + top[1] + top[2] == target:
                count += 1
            result = top[0]
            if stack:
                parent = stack[-1]
                parent[1 + parent[3]] = result
                parent[3] += 1
            continue
        x = read()
        if x is None:
            top[3] += 1  # missing child slot stays None
        else:
            stack.append([x, None, None, 0])
    return count
