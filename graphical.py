#!/usr/bin/python3

import math
import sys
import os
import pygame
import random
import time

from resources import weapons
from resources.game_logic import GameLogic


BLACK = pygame.Color(0, 0, 0)
GREY = pygame.Color(120, 120, 120)

RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
GREEN = pygame.Color(0, 255, 0)

TAU = math.pi * 2


pygame.init()
window = pygame.display.set_mode((800, 600))

imgLoad = pygame.image.load
nuclearIcon = imgLoad("images/nuclear.png").convert_alpha()
pygame.display.set_icon(nuclearIcon)

SANS_FONT = pygame.font.Font("fonts/OpenSans-Regular.ttf", 14)
TITLE_FONT = pygame.font.Font("fonts/OpenSans-Regular.ttf", 24)


def load_explosions():
    explosions = []
    path = "images/explosions"

    for i in range(1, 16):
        file = str(i) + ".png"

        file_path = os.path.join(path, file)
        image = imgLoad(file_path).convert_alpha()
        rect = image.get_rect()

        explosions.append({
            "Image": image,
            "Rect": rect
        })

    return explosions


explosionImages = load_explosions()


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


class AnimatedWeapon:
    COLORS = {
        weapons.Weapons.LASER: YELLOW,
        weapons.Weapons.MISSILE: GREEN,
        weapons.Weapons.NUKE: RED
    }

    def __init__(self, start, end, event, turn_length):
        self.start, self.end = start, end

        self.rect = pygame.Rect(0, 0, 10, 10)
        self.start_time = time.time() + turn_length * random.random()
        self.event = event
        self.weapon = event["Weapon"]
        self.turn_length = turn_length
        self.remove = False

    def get_pos(self):
        sx, sy = self.start
        ex, ey = self.end

        delta = (time.time() - self.start_time) / self.get_max_time()

        x = sx + (ex - sx) * delta
        y = sy + (ey - sy) * delta

        self.rect.center = x, y

    def draw(self, window):
        if time.time() > self.start_time:
            self.get_pos()
            window.fill(self.COLORS[self.weapon], self.rect)

        if time.time() - self.start_time > self.get_max_time():
            self.remove = True

    def get_max_time(self):
        return (self.weapon.value.SPEED + 1) * self.turn_length


class TextRect:
    def __init__(self, font, text, foreColour):
        self.font = font

        self.last_text = None
        self.text = text

        self.foreColour = foreColour

        self.rect = None
        self.check_update()

    def check_update(self):
        if self.text != self.last_text:
            #Antialias is True
            self.surface = self.font.render(self.text, True, self.foreColour)
            self.last_text = self.text
            self.realignRect()

    def draw(self, window):
        self.check_update()
        window.blit(self.surface, self.rect)

    def realignRect(self):
        if not self.rect:
            self.rect = self.surface.get_rect()

        old_center = self.rect.center

        self.rect.size = self.surface.get_size()
        self.rect.center = old_center


class Player:
    HEIGHT = 80
    WIDTH = 80

    BORDER_COLOUR = pygame.Color(0, 0, 100)

    def __init__(self, country, posx=0, posy=0):
        self.country = country
        self.health = country.health

        self.border = pygame.Rect(0, 0, self.HEIGHT, self.WIDTH)
        self.inner = pygame.Rect(0, 0, self.HEIGHT - 10, self.WIDTH - 10)

        display_name = self.country.name.replace("_", " ").title()
        self.name = TextRect(SANS_FONT, display_name, GREY)
        self.health_text = TextRect(SANS_FONT, str(self.health), RED)
        self.nuke_text = TextRect(SANS_FONT, str(self.country.nukes), GREEN)

        self.set_pos(posx, posy)

    def draw(self, window: pygame.Surface):
        window.fill(self.BORDER_COLOUR, self.border)
        window.fill(BLACK, self.inner)

        if self.health:
            self.health_text.text = str(object=self.health)
            self.health_text.check_update()

            self.nuke_text.text = str(self.country.nukes)
            self.nuke_text.check_update()

            self.name.draw(window)
            self.nuke_text.draw(window)
            self.health_text.draw(window)

    def set_pos(self, posx, posy):
        self.border.center = posx, posy
        self.inner.center = posx, posy

        self.name.rect.midbottom = self.border.midtop
        self.health_text.rect.midbottom = self.name.rect.midtop
        self.nuke_text.rect.center = posx, posy

    def apply_weapon(self, e: AnimatedWeapon):
        self.take_damage(e.weapon.value.DAMAGE)

    def take_damage(self, damage: int):
        if self.health > 0:
            self.health -= damage

            if self.health <= 0:
                self.health = 0


class PyGame:
    FPS = 30
    WIDTH = 800
    HEIGHT = 600
    TURN_LENGTH = 3

    def __init__(self, window):
        self.game = GameLogic()
        self.window = window
        self.clock = pygame.time.Clock()
        self.active_weapons = []
        self.explosions = []
        self.timer = time.time()

        self.countries = []
        country_count = len(self.game.countries)

        for i, c in enumerate(self.game.countries):
            perc = (math.sin(i * TAU / country_count) / 2 + 1/2)
            x = (0.1 + 0.8 * perc) * self.WIDTH

            perc = (math.cos(i * TAU / country_count) / 2 + 1/2)
            y = (0.1 + 0.8 * perc) * self.HEIGHT

            self.countries.append(Player(c, x, y))

    def start(self):
        running = True
        self.turn_surface = TITLE_FONT.render("Round " + str(self.game.turn),
                                              True, GREY)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return 0

            # Refresh screen
            self.window.fill(BLACK)
            self.window.blit(self.turn_surface, (0, 0))

            # Draw countries
            for c in self.countries:
                c.draw(self.window)

            for e in self.explosions[:]:
                e.draw(self.window)
                if not e.frame:
                    self.explosions.remove(e)

            for e in self.active_weapons[:]:
                e.draw(self.window)
                if e.remove:
                    self.active_weapons.remove(e)
                    self.countries[e.event["Target"]].apply_weapon(e)

                    if e.weapon is weapons.Weapons.NUKE:
                        self.explosions.append(Explosion(e.rect.center))
                    elif e.weapon is weapons.Weapons.MISSILE:
                        self.explosions.append(Explosion(e.rect.center, frame=5))

            if time.time() - self.timer > self.TURN_LENGTH * self.game.turn:
                if (self.game.get_alive_count() > 1
                        and self.game.turn <= self.game.MAX_TURNS):

                    self.game.do_turn()
                    self.animate_turn()
                    self.turn_surface = TITLE_FONT.render("Round " + str(self.game.turn),
                                                          True, GREY)

                # Finish weapon animations
                elif not self.active_weapons:
                    break

            pygame.display.update()
            self.clock.tick(self.FPS)

        if self.game.get_alive_count() == 1:
            alive = self.game.get_alive_countries()[0]
            print(self.game.countries[alive].name, "is the last one standing.")

        else:
            print("There were no survivors.")

        input()

    def animate_turn(self):
        for event in self.game.events:
            if "Source" in event and "Target" in event:
                start = self.countries[event["Source"]].inner.center
                end = self.countries[event["Target"]].inner.center

                self.active_weapons.append(AnimatedWeapon(start, end, event,
                                                          self.TURN_LENGTH))


if __name__ == "__main__":
    active_game = PyGame(window)
    active_game.start()
