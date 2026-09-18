# Per major part: keep first m-1 minors compressed, merge the rest of the raw text into one token.
def compressBounded(s: str, m: int) -> str:
    def comp(w: str) -> str:
        return w[0] + str(len(w) - 2) + w[-1]

    out = []
    for major in s.split('/'):
        minors = major.split('.')
        if len(minors) <= m:
            tokens = [comp(w) for w in minors]
        else:
            tokens = [comp(w) for w in minors[:m - 1]]
            tokens.append(comp(''.join(minors[m - 1:])))
        out.append('.'.join(tokens))
    return '/'.join(out)
