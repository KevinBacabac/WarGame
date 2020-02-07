from random import choice
from typing import Dict, List


from resources.weapons import Weapons


class Bot:
    """
    If you fire a laser it will fire a laser
    If you nuke it- it'll try too..

    A bot that always fires at the last enemy
    """

    def __init__(self):
        self.last_enemy = None
        self.last_weapon = None

    def action(self, country_status: Dict, world_state: Dict):
        # Did anyone fire at it
        self.review_events(world_state["events"], country_status["ID"])

        # Fire at a target if there is one
        if self.last_enemy is not None and self.last_weapon is not None:
            action, target = self.last_weapon, self.last_enemy

            return {
                "Weapon": action,
                "Target": target,
                "Type": "Attack",
            }

        return {}

    def review_events(self, events: Dict, self_id: int):
        for event in events["Player"]:
            # Search for only events that fire at this bot
            if event["Type"] == "Attack":
                attack = event
                if attack["Target"] == self_id:
                    self.last_enemy = attack["Source"]
                    self.last_weapon = attack["Weapon"]
                    break
