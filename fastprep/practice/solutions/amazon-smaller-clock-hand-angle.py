# Approach: compute each hand's absolute degree position (hour hand moves 0.5 deg/min) and take the smaller arc.
def clockAngle(hour: int, minutes: int) -> float:
    hour_pos = (hour % 12) * 30.0 + minutes * 0.5
    minute_pos = minutes * 6.0
    diff = abs(hour_pos - minute_pos)
    return min(diff, 360.0 - diff)
