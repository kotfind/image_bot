from PIL import Image
import tempfile
import config
import numpy as np
from math import inf

from Ray import Ray
from Sphere import Sphere
from Material import Material
from Light import Light

backgroundColor = (255, 255, 255)

scene = [
    Sphere(np.array([   5, -3, 10]),    3, Material(np.array([ 255,    0,    0]))),
    Sphere(np.array([   1, -3,  5]),    1, Material(np.array([   0,  255,    0]))),
    Sphere(np.array([  -1,  1,  8]),    1, Material(np.array([   0,    0,  255]))),
    Sphere(np.array([  -3,  3,  2]),    2, Material(np.array([   0,  255,  255]))),
]

lights = [
    Light(np.array([    1,  -3, -2]),    1),
    Light(np.array([    0,  0,  1]),   0.3),
]

def getPixel(x, y):
    '''
        x and y in range (-1; 1)
    '''

    ray = Ray(
        np.array([0, 0, 0]),
        np.array([x, y, 1])
    )

    # Intersection
    sceneDist = inf
    sphere = None
    for s in scene:
        if (t := ray.intersect(s)) < sceneDist:
            sceneDist = t
            sphere = s

    if sphere is None:
        return backgroundColor

    pt = ray(sceneDist)
    norm = sphere.norm(pt)

    # Light
    diffuseLightIntensity = 0
    for light in lights:
        lightDir = light.pos - pt
        lightDir /= np.linalg.norm(lightDir)
        diffuseLightIntensity += light.intensity * max(0, abs(np.dot(norm, lightDir)))

    return sphere.m.diffuseColor * diffuseLightIntensity

def genImage(date):
    '''
        Returns file object of created image
    '''

    img = Image.new('RGB', config.size)
    pix = img.load()

    wid, hei = config.size
    for x in range(wid):
        for y in range(hei):
            pix[x, y] = tuple(map(int, getPixel(
                2 * x / wid - 1,
                1 - 2 * y / hei
            )))

    file = tempfile.TemporaryFile()
    img.save(file, 'JPEG')
    return file
