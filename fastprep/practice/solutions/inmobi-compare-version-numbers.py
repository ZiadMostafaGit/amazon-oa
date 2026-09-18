# Split on dots and compare revision integers pairwise, padding missing revisions with 0.
def compareVersion(version1: str, version2: str) -> int:
    a = version1.split('.')
    b = version2.split('.')
    n = max(len(a), len(b))
    for i in range(n):
        x = int(a[i]) if i < len(a) and a[i] != '' else 0
        y = int(b[i]) if i < len(b) and b[i] != '' else 0
        if x < y:
            return -1
        if x > y:
            return 1
    return 0
