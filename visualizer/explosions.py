import os
import pygame


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
    def __init__(self, pos, frame=None):
        self.pos = pos

        if frame:
            self.frame = frame
        else:
            self.frame = len(explosionImages) - 1

    def draw(self, window):
        explosion = explosionImages[self.frame]
        rect = explosion["Rect"]

        x, y = self.pos
        x -= rect.width / 2
        y -= rect.height / 2

        window.blit(explosion["Image"], (x, y))
        self.frame -= 1


explosionImages = load_explosions()
