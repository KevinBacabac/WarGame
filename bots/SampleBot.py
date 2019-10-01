from resources.weapons import Weapons


from random import randint


class Bot:
    def __init__(self):
        pass

    def action(self, country_status: dict, world_history: dict):
        weapon = randint(1, 3)
        target = randint(1, world_history["player_count"])
