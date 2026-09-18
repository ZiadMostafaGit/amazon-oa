# Walk the query index back through the rounds: each char x expands to x + '0',
# so index >> rounds picks the originating character and the low bits must all be zero.
def solve(bits: str, rounds: int, index: int) -> int:
    n = len(bits)
    # Avoid building 2**rounds when rounds is huge: index's bit length bounds the useful shift.
    shift = rounds
    if shift > index.bit_length():
        # index >> shift == 0 and the low `shift` bits are exactly index
        origin = 0
        offset = index
    else:
        origin = index >> shift
        offset = index & ((1 << shift) - 1)
    if origin >= n or origin < 0:
        return 0
    if offset != 0:
        return 0
    return 1 if bits[origin] == '1' else 0
