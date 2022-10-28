import numpy as np
from math import inf, sqrt

class Ray:
    def __init__(s, o, d):
        s.o = o
        s.d = d / np.linalg.norm(d)

    def __call__(s, t):
        return s.o + t * s.d

    def intersect(s, w):
        k = s.o - w.o

        a = s.d[0]**2 + s.d[1]**2 + s.d[2]**2
        b = 2 * (k[0] * s.d[0] + k[1] * s.d[1] + k[2] * s.d[2])
        c = k[0]**2 + k[1]**2 + k[2]**2 - w.r**2

        d = b**2 - 4 * a * c

        if d < 0:
            return inf
        else:
            t1 = (-b - sqrt(d)) / (2 * a)
            t2 = (-b + sqrt(d)) / (2 * a)

            if t2 < 0:
                return inf
            elif t1 > 0:
                return t1
            else:
                return t2 # XXX
