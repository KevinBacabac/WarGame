from enum import Enum, unique


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


@unique
class Weapons(Enum):
    LASER = Laser
    MISSILE = Missile
    NUKE = Nuke
