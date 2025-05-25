import math

def modulo(a, b):
    return a - int(a / b) * b


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def min_distance(x_ref, y_ref, list_points):
    distances = [get_distance(x_ref, y_ref, point[0], point[1]) for point in list_points]
    minimum = min(distances)

    return minimum, distances.index(minimum)