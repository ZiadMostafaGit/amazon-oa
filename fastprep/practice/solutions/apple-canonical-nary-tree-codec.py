# Iterative stack parse of the grammar into N-ary nodes, then an iterative post-order-free re-serialization.
def canonicalizeNaryTree(data: str) -> str:
    n = len(data)
    i = 0
    root = None
    stack = []  # list of [value, children]
    while i < n:
        c = data[i]
        if c.isspace() or c == ',':
            i += 1
        elif c == '[':
            i += 1
        elif c == ']':
            node = stack.pop()
            if not stack:
                root = node
            i += 1
        else:
            j = i
            if data[j] in '+-':
                j += 1
            while j < n and data[j].isdigit():
                j += 1
            value = int(data[i:j])
            node = [value, []]
            if stack:
                stack[-1][1].append(node)
            stack.append(node)
            i = j
    if root is None:
        return ""

    parts = []
    # frames: (node, child index)
    frames = [[root, 0]]
    parts.append(str(root[0]))
    parts.append('[')
    while frames:
        frame = frames[-1]
        node, idx = frame
        children = node[1]
        if idx < len(children):
            frame[1] = idx + 1
            if idx:
                parts.append(',')
            child = children[idx]
            parts.append(str(child[0]))
            parts.append('[')
            frames.append([child, 0])
        else:
            parts.append(']')
            frames.pop()
    return ''.join(parts)
