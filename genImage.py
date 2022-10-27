from PIL import Image
import tempfile
import config
import numpy as np
from math import sqrt

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
            return None
        else:
            t1 = (-b - sqrt(d)) / (2 * a)
            t2 = (-b + sqrt(d)) / (2 * a)

            if t2 < 0:
                return None
            elif t1 > 0:
                return s(t1)
            else:
                return s(t2) # XXX

class Sphere:
    def __init__(s, o, r):
        s.o = o
        s.r = r

    def norm(s, p):
        n = p - s.o
        return n / np.linalg.norm(n)

def scene(ray):
    spheres = [
        Sphere(np.array([5, 3, 10]), 3),
        Sphere(np.array([1, 3, 5]), 1),
        Sphere(np.array([-1, -1, 8]), 1),
        Sphere(np.array([-3, -3, 2]), 2),
    ]

    intersections = [] # pair of point and normal

    for sphere in spheres:
        if (pt := ray.intersect(sphere)) is not None:
            intersections.append((pt, sphere.norm(pt)))

    if not intersections:
        return None

    return min(intersections, key=lambda tup: np.linalg.norm(tup[0] - ray.o))

def getPixel(x, y):
    '''
        x and y in range (-1; 1)
    '''

    ray = Ray(
        np.array([0, 0, 0]),
        np.array([x, y, 1])
    )

    tmp = scene(ray)
    if tmp is None:
        return (255, 255, 255)

    pt, norm = tmp

    r = int(255 * abs(np.dot(ray.d, norm)))
    return (r, 0, 0)

def genImage(date):
    '''
        Returns file object of created image
    '''

    img = Image.new('RGB', config.size)
    pix = img.load()

    wid, hei = config.size
    for x in range(wid):
        for y in range(hei):
            pix[x, y] = getPixel(
                2 * x / wid - 1,
                2 * y / hei - 1
            )

    file = tempfile.TemporaryFile()
    img.save(file, 'JPEG')
    return file
