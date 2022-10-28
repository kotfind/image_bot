import numpy as np
from math import sin

from Ray import Ray
from Sphere import Sphere
from Material import Material
import config

def rand(r):
    return sin(r * 234291 + 123123) % 1

def rand2(r1, r2):
    return sin(r1 * 230931 + r2 * 604302 + 237491) % 1

def rand3(r1, r2, r3):
    return sin(r1 * 532843 + r2 * 128303 + r3 * 230495 + 184207) % 1

def getBackgroundColor(seed, d):
    seed = rand(seed)
    color = np.array([0.] * 3)
    for i in range(3):
        a = rand3(seed, i, 1) * 8 + 2
        b = rand3(seed, i, 2) * 4
        c = rand3(seed, i, 3) * 8 + 2
        f = rand3(seed, i, 4) * 4
        color[i] = sin(d[0] * a + b) + sin(d[1] * c + f)
    return abs(color) * 100 + 55

def getSpheres(seed):
    seed = rand(seed)

    scene = []
    for i in range(config.spheresN):
        pos = np.array([0.] * 3)
        pos[0] = (rand3(seed, i, 1) - 0.5) * 23
        pos[1] = (rand3(seed, i, 2) - 0.5) * 23
        pos[2] = rand3(seed, i, 3) * 20 + 15

        radius = rand3(seed, i, 4) * 5 + 0.5

        albedo = np.array([0.] * 3)
        if rand3(seed, i, 5) > 0.3: # mirror
            albedo[0] = rand3(seed, i, 6) * 0.1 + 0.1 # diffuse
            albedo[1] = rand3(seed, i, 7) * 0.4 + 0.5 # specular
            albedo[2] = rand3(seed, i, 8) * 0.3 + 0.6 # reflected

            specExp = rand3(seed, i, 12) * 50 + 30

        else: # not mirror
            albedo[0] = rand3(seed, i, 6) * 0.5 + 0.5 # diffuse
            albedo[1] = rand3(seed, i, 7) * 0.2 + 0.0 # specular
            albedo[2] = 0 # reflected

            specExp = rand3(seed, i, 12) * 10 + 1

        color = np.array([0.] * 3)
        for j in range(3):
            color[j] = rand3(seed, i, 9 + j) * 200 + 55

        scene.append(Sphere(
            pos,
            radius,
            Material(
                albedo,
                color,
                specExp
            )
        ))

    return scene
