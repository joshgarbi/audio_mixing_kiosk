
def within_margin(value, target, margin):
    upper = target + (target * margin / 100)
    lower = target - (target * margin / 100)
    return lower <= value <= upper