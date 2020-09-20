def positionInRange(value, min, max, clamp=True):

    if min == max:
        # If the price is stable cheap is very favourable
        if value < min:
            return 0.0
        if value > min:
            return 1.0
        if value == min:
            return 0.5

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
