from PIL import Image
import tempfile
import config
import numpy as np
from math import inf
from Ray import Ray
from Sphere import Sphere

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
