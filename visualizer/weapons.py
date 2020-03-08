import pygame
import random
import time
from typing import Dict, Tuple

from resources import weapons
from visualizer.collection import Collection
from visualizer.timer import Timer


class AnimatedWeapon:
    __slots__ = ("start", "end", "rect", "event", "turn_length", "weapon",
                 "timer", "trail")

    def __init__(self, start: Tuple[int, int], end: Tuple[int, int],
                 event: Dict, turn_length: int):
        self.start, self.end = start, end

        self.rect = pygame.Rect(0, 0, 10, 10)
        self.event = event
        self.turn_length = turn_length
        self.weapon = event["Weapon"]

        self.timer = Timer(self.get_max_time())
        self.trail = Trail(self._get_colour())

    def get_pos(self):
        sx, sy = self.start
        ex, ey = self.end

        delta = self.timer.get_delta()

        x = sx + (ex - sx) * delta
        y = sy + (ey - sy) * delta

        self.rect.center = x, y

    def draw(self, window):
        dirty_rects = []

        if time.time() > self.timer.start_time:
            dirty_rects.append(self.rect.copy())
            dirty_rects.append(self.rect)

            self.get_pos()
            window.fill(self._get_colour(), self.rect)
            dirty_rects += self.trail.draw(window, self.rect.center)

        return dirty_rects

    def get_max_time(self):
        return self.weapon.value.SPEED * self.turn_length

    def _get_colour(self):
        return pygame.Color(*self.weapon.value.COLOUR)

    def resize(self, start: Tuple[int, int], end: Tuple[int, int]):
        self.start, self.end = start, end


class Trail:
    COUNT = 5
    INTERVAL = 1/10

    def __init__(self, colour):
        self.colour = colour
        self.last_pos = []
        self.counter = time.time()

    def draw(self, window, new_pos: Tuple[int, int]):
        dirty_rects = self._update(new_pos)

        # Draw trail
        if len(self.last_pos) > 1:
            for point in self.last_pos:
                pygame.draw.circle(window, self.colour, point, 2)
                dirty_rects.append(self._get_rect(point))

        return dirty_rects

    def _update(self, new_pos: Tuple[int, int]):
        dirty_rects = []

        now = time.time()
        if self.counter <= now:
            self.counter += self.INTERVAL
            self.last_pos.append(new_pos)

            while len(self.last_pos) > self.COUNT:
                dirty_rects.append(self._get_rect(self.last_pos[0]))
                del self.last_pos[0]

        return dirty_rects

    @staticmethod
    def _get_rect(pos):
        x, y = pos
        x -= 2
        y -= 2

        return pygame.Rect(x, y, 5, 5)


class ActiveWeapons(Collection):
    class_type = AnimatedWeapon

    def draw(self, window):
        dirty_rects = []

        for e in self.all[:]:
            dirty_rects += e.draw(window)
            if e.timer.is_done():
                dirty_rects.append(e.rect)
                self.all.remove(e)

        return dirty_rects
