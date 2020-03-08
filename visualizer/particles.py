import pygame
import random

from math import sin, cos, pi
from typing import Tuple

from visualizer.collection import Collection

TAU = 2 * pi


class Particle:
    def __init__(self, pos: Tuple[int, int]):
        self.x, self.y = pos
        self.rect = pygame.Rect(0, 0, 5, 5)

        angle = random.uniform(0, TAU)
        speed = random.uniform(0.05, 2)

        self.dx = cos(angle) * speed
        self.dy = sin(angle) * speed

        self.despawn_count = random.uniform(0, 1)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.colour = pygame.Color(r, g, b)

    def draw(self, window, FPS):
        dirty_rects = []

        dirty_rects.append(self.rect.copy())
        dirty_rects.append(self.rect)

        self.x += self.dx
        self.y += self.dy
        self.rect.center = self.x, self.y

        window.fill(self.colour, self.rect)
        self.despawn_count -= 1 / FPS

        return dirty_rects


class Particles(Collection):
    class_type = Particle

    def add(self, pos):
        for i in range(100):
            self.all.append(Particle(pos))

    def draw(self, window, FPS):
        dirty_rects = []

        for p in self.all[:]:
            dirty_rects += p.draw(window, FPS)
            if p.despawn_count <= 0:
                dirty_rects.append(p.rect)
                self.all.remove(p)

        return dirty_rects
