import numpy as np

class Sphere:
    def __init__(s, o, r):
        s.o = o
        s.r = r

    def norm(s, p):
        n = p - s.o
        return n / np.linalg.norm(n)
