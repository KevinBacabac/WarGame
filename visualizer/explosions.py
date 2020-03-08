import os
import pygame

from typing import Tuple

from visualizer.collection import Collection


def load_explosions():
    explosions = []
    path = "images/explosions"

    for i in range(1, 16):
        file = str(i) + ".png"

        file_path = os.path.join(path, file)
        image = pygame.image.load(file_path).convert_alpha()
        rect = image.get_rect()

        explosions.append({
            "Image": image,
            "Rect": rect
        })

    return explosions


class Explosion:
    def __init__(self, pos: Tuple[int, int], weapon):
        self.pos = pos
        self.frame = weapon.value.EXPLOSION_SIZE

    def draw(self, window):
        dirty_rects = []

        explosion = explosionImages[self.frame]
        rect = explosion["Rect"]

        x, y = self.pos
        x -= rect.width / 2
        y -= rect.height / 2

        rect = window.blit(explosion["Image"], (x, y))
        self.frame -= 1

        dirty_rects.append(rect)
        return dirty_rects


class Explosions(Collection):
    class_type = Explosion

    def draw(self, window):
        dirty_rects = []

        for e in self.all[:]:
            dirty_rects += e.draw(window)
            if not e.frame:
                self.all.remove(e)

        return dirty_rects


explosionImages = load_explosions()
