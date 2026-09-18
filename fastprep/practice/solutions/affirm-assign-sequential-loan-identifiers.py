# Direct enumeration: the i-th transaction gets identifier i + 1.
from typing import List, Optional, Any


def assignLoanIds(transactionRefs: List[str]) -> List[int]:
    return list(range(1, len(transactionRefs) + 1))
