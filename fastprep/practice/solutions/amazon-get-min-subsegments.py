# Segment borders fall on even indices, so work pairwise: "01"/"10" pairs are free, pure pairs fix a colour.
def getminSubsegments(frames: str) -> int:
    segments = 0
    last = None  # colour forced by the previous pure pair
    for i in range(0, len(frames) - 1, 2):
        a = frames[i]
        b = frames[i + 1]
        if a != b:
            continue  # mixed pair: one flip either way, so it adopts a neighbour's colour
        if a != last:
            segments += 1
            last = a
    return segments if segments else 1
