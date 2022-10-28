from PIL import Image
import tempfile
import config
import numpy as np
from math import inf, sin

from Ray import Ray
from Sphere import Sphere
from Material import Material
from Light import Light

scene = [
    Sphere(np.array([   5, -3, 10]),    3, Material(np.array([0.1, 0.2, 0.7]), np.array([ 255,    0,    0]), 50)),
    Sphere(np.array([   1, -3,  5]),    1, Material(np.array([0.6, 0.3, 0.0]), np.array([   0,  255,    0]), 50)),
    Sphere(np.array([  -1,  1,  8]),    1, Material(np.array([0.9, 0.1, 0.4]), np.array([   0,    0,  255]), 10)),
    Sphere(np.array([  -3,  3,  2]),    2, Material(np.array([0.9, 0.1, 0.1]), np.array([   0,  255,  255]), 10)),
]

lights = [
    Light(np.array([    1,  -3, -2]),    1),
    Light(np.array([    0,  0,  1]),   0.3),
]

maxDepth = 4

def getBackgroundColor(d):
    r = sin(d[0] * 10 + 0.2) + sin(d[1] * 5 + 0.5)
    g = sin(d[0] * 6 + 0.3) + sin(d[1] * 2 + 0.7)
    b = sin(d[0] * 3 + 0.2) + sin(d[1] * 10 + 0.1)
    return abs(np.array([r, g, b])) * 100 + 55

def reflect(I, N):
    return I - 2 * N * np.dot(N, I)

def castRay(ray, depth = 0):
    # Intersection
    sceneDist = inf
    sphere = None
    for s in scene:
        if (t := ray.intersect(s)) < sceneDist:
            sceneDist = t
            sphere = s

    if depth > maxDepth or sphere is None:
        return getBackgroundColor(ray.d)

    pt = ray(sceneDist)
    norm = sphere.norm(pt)

    # Reflect
    reflectDir = reflect(ray.d, norm)
    reflectedColor = castRay(
        Ray(
            pt + norm * (1e-3 if np.dot(reflectDir, norm) > 0 else -1e-3),
            reflectDir
        ),
        depth + 1
    )

    # Light
    diffuseLightIntensity = 0
    specularLightIntensity = 0

    for light in lights:
        lightDir = light.pos - pt
        lightDir /= np.linalg.norm(lightDir)
        diffuseLightIntensity += light.intensity * max(0, abs(np.dot(norm, lightDir)))

        specularLightIntensity += max(0, np.dot(reflect(lightDir, norm), ray.d)) ** sphere.m.specularExponent * light.intensity

    return sphere.m.diffuseColor * diffuseLightIntensity * sphere.m.albedo[0] + \
        np.array([255] * 3) * specularLightIntensity * sphere.m.albedo[1] + \
        reflectedColor * sphere.m.albedo[2]

def genImage(date):
    '''
        Returns file object of created image
    '''

    img = Image.new('RGB', config.size)
    pix = img.load()

    wid, hei = config.size
    for x in range(wid):
        for y in range(hei):
            ray = Ray(
                np.array([0, 0, 0]),
                np.array([
                    2 * x / wid - 1,
                    1 - 2 * y / hei,
                    1
                ])
            )
            pix[x, y] = tuple(map(int, castRay(ray)))

    file = tempfile.TemporaryFile()
    img.save(file, 'JPEG')
    return file
