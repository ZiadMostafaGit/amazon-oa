# Walk month by month from the known Jan 1, 2000 Saturday anchor, tracking weekday mod 7.
def countSundayMonthStarts(startYear: int, endYear: int) -> int:
    def is_leap(y: int) -> bool:
        return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)

    lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dow = 6  # 0 = Sunday ... 6 = Saturday; Jan 1, 2000 was a Saturday
    count = 0
    for year in range(2000, endYear + 1):
        for month in range(12):
            if year >= startYear and dow == 0:
                count += 1
            days = 29 if (month == 1 and is_leap(year)) else lengths[month]
            dow = (dow + days) % 7
    return count
