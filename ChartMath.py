from collections import Counter
from numpy import pi


color_names = ["red", "green", "blue", "orange", "yellow", "black", "pink", "brown"]


def compute_color_distribution(start_angle_key, end_angle_key, color_key, colors):
    lenum = len(colors)
    color_counts = Counter(colors)
    percents = [0]
    for key in color_names:
        aggregate = percents[-1] + color_counts[key]/float(lenum)
        percents.append(aggregate)

    starter = [perc*2*pi for perc in percents[:-1]]
    ender = [perc*2*pi for perc in percents[1:]]
    print color_counts
    print percents
    return {start_angle_key: starter, end_angle_key: ender, color_key: color_names}

