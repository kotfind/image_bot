import numpy as np
from math import sin

from Ray import Ray
from Sphere import Sphere
from Material import Material

def getBackgroundColor(seed, d):
    r = sin(d[0] * 10 + 0.2) + sin(d[1] * 5 + 0.5)
    g = sin(d[0] * 6 + 0.3) + sin(d[1] * 2 + 0.7)
    b = sin(d[0] * 3 + 0.2) + sin(d[1] * 10 + 0.1)
    return abs(np.array([r, g, b])) * 100 + 55


def getSpheres(seed):
    return [
        Sphere(np.array([   5, -3, 10]),    3, Material(np.array([0.1, 0.2, 0.7]), np.array([ 255,    0,    0]), 50)),
        Sphere(np.array([   1, -3,  5]),    1, Material(np.array([0.1, 0.2, 0.7]), np.array([   0,  255,    0]), 50)),
        Sphere(np.array([  -1,  1,  8]),    1, Material(np.array([0.1, 0.2, 0.7]), np.array([   0,    0,  255]), 10)),
        Sphere(np.array([  -3,  3,  2]),    2, Material(np.array([0.1, 0.2, 0.7]), np.array([   0,  255,  255]), 10)),
    ]
