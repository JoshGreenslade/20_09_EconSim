def positionInRange(value, min, max, clamp=True):

    value -= min
    max -= min
    min = 0
    value = (value / (max-min))
    if clamp:
        if value < 0:
            value = 0
        if value > 1:
            value = 1
    return value
