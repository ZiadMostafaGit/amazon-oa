# Split on '/' then '.', compress each minor part to first + middle-count + last, rejoin.
def compress(s: str) -> str:
    def comp(w: str) -> str:
        return w[0] + str(len(w) - 2) + w[-1]

    majors = s.split('/')
    out = []
    for major in majors:
        out.append('.'.join(comp(m) for m in major.split('.')))
    return '/'.join(out)
