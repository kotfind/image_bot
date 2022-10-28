from PIL import Image
import tempfile
import config
import numpy as np
from math import sqrt, inf

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

class Sphere:
    def __init__(s, o, r):
        s.o = o
        s.r = r

    def norm(s, p):
        n = p - s.o
        return n / np.linalg.norm(n)

scene = [
    Sphere(np.array([5, 3, 10]), 3),
    Sphere(np.array([1, 3, 5]), 1),
    Sphere(np.array([-1, -1, 8]), 1),
    Sphere(np.array([-3, -3, 2]), 2),
]

def getPixel(x, y):
    '''
        x and y in range (-1; 1)
    '''

    ray = Ray(
        np.array([0, 0, 0]),
        np.array([x, y, 1])
    )

    sphereDist = inf
    sphere = None
    for s in scene:
        if (t := ray.intersect(s)) < sphereDist:
            sphereDist = t
            sphere = s

    if sphere is None:
        return (255, 255, 255)

    r = int(255 * abs(np.dot(ray.d, sphere.norm(ray(sphereDist)))))
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
