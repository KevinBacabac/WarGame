from enum import Enum


class Weapons(Enum):
    LASER = 1
    MISSILE = 2
    NUKE = 3


class Laser:
    COST = 10
    DAMAGE = 20
    SPEED = 1
    REVEAL_CHANCE = 1


class Missile:
    COST = 10
    DAMAGE = 20
    SPEED = 3
    REVEAL_CHANCE = 0.25


class Nuke:
    DAMAGE = 100
    SPEED = 3
    REVEAL_CHANCE = 1
