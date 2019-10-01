from random import randint

from resources.weapons import Weapons


class Bot:
    def __init__(self):
        pass

    def action(self, country_status: dict, world_state: dict):
        weapon = randint(1, 3)
        target = randint(1, world_state["player_count"])

        return {
            "Weapon": weapon,
            "Target": target
        }
