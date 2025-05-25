import math

def modulo(a, b):
    return a - int(a / b) * b


def get_distance(x1, y1, x2, y2):
    math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)