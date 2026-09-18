# Direct deterministic simulation: round-robin deal, sorted hands, first-legal-card play, trick scoring.
RANKS = "23456789TJQKA"
SUITS = "CDHS"
POINTS = {"5": 5, "T": 10, "K": 13}


def simulateTrickTakingGame(deckOrder: str) -> str:
    deck = deckOrder.split()

    hands = [[], [], [], []]
    for i, card in enumerate(deck):
        hands[i % 4].append(card)

    for h in hands:
        h.sort(key=lambda c: (SUITS.index(c[1]), RANKS.index(c[0])))

    scores = [0, 0, 0, 0]
    leader = 0

    for _ in range(13):
        played = []  # (player, card)
        lead_suit = None
        for turn in range(4):
            p = (leader + turn) % 4
            hand = hands[p]
            idx = 0
            if lead_suit is not None:
                idx = -1
                for k, c in enumerate(hand):
                    if c[1] == lead_suit:
                        idx = k
                        break
                if idx == -1:
                    idx = 0
            card = hand.pop(idx)
            if lead_suit is None:
                lead_suit = card[1]
            played.append((p, card))

        winner = None
        best_rank = -1
        pot = 0
        for p, card in played:
            pot += POINTS.get(card[0], 0)
            if card[1] == lead_suit:
                r = RANKS.index(card[0])
                if r > best_rank:
                    best_rank = r
                    winner = p
        scores[winner] += pot
        leader = winner

    top = max(scores)
    winners = [i for i in range(4) if scores[i] == top]
    return "scores=[" + ",".join(map(str, scores)) + "];winners=[" + ",".join(map(str, winners)) + "]"
