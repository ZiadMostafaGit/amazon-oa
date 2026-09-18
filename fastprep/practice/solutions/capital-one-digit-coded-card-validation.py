# Direct flag decoding: read the encoded bits at fixed positions and apply the network rules.
from typing import List, Optional, Any


def validatePayments(cardNumbers: List[str], transactionIds: List[str], amounts: List[int]) -> List[bool]:
    out = []
    for card, tid, amount in zip(cardNumbers, transactionIds, amounts):
        multi_use = card[13] == '1'
        is_master = card[14] == '1'
        merchant_bound = card[15] == '1'
        is_charge = tid[6] == '1'
        is_online = tid[7] == '1'

        if is_master:
            valid = (not merchant_bound and amount < 100) or (merchant_bound and amount > 100)
        else:
            valid = (merchant_bound and multi_use) or (is_online and is_charge and amount < 100)
        out.append(bool(valid))
    return out
