from random import choice

from resources.weapons import Weapons


class Bot:
    """
    If you fire a laser it will fire a laser
    If you nuke it- don't expect a response

    A bot that always fires at the last enemy
    """

    def __init__(self):
        self.last_enemy = None
        self.last_weapon = None


    def action(self, country_status: dict, world_state: dict):
        # Did anyone fire at it
        self.review_events(world_state["events"], country_status["ID"])

        # Fire at a target if there is one
        if self.last_enemy is not None and self.last_weapon is not None:
            action, target = self.last_weapon, self.last_enemy

            return {
                "Action": action,
                "Target": target
            }

        else:
            return {}


    def review_events(self, events, self_id):
        for event in events:
            # Search for only events that fire at this bot
            if event["Action"] in Weapons and event["Target"] == self_id:
                self.last_enemy = event["Source"]
                self.last_weapon = event["Action"]
                break
