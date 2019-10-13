from typing import List
from os.path import abspath, dirname
import importlib
import os


from resources import country, weapons


class GameLogic:
    MAX_TURNS = 30

    def __init__(self):
        self.countries = get_countries()
        self.events = []

        # Initialize ids
        for i, country in enumerate(self.countries):
            country.id = i

        self.turn = 1


    def do_turn(self):
        print("Round", self.turn)
        actions = self._get_actions()
        self._run_actions(actions)
        self.turn += 1

    def get_alive_count(self):
        """ Returns an integer """
        return sum(country.alive for country in self.countries)


    def get_alive_countries(self):
        """ Returns indexes """
        return [pos for pos, country in enumerate(self.countries) if country.alive]


    def _get_world_state(self):
        return {
            "countries": self._serialize_countries(),
            "events": self.events,
            "alive_players": self.get_alive_countries()
        }


    def _get_actions(self):
        actions = []
        world_state = self._get_world_state()

        for i, country in enumerate(self.countries):
            if not country.alive:
                continue

            action = country.get_action(world_state)

            # Check if action is valid
            # If action is invalid, nuke own country
            if not self._is_valid_action(action):
                action = {}

            actions.append(action)

        return actions


    def _is_valid_action(self, action: dict):
        try:
            if "Weapon" not in action:
                return True

            return all((
                action["Weapon"] in weapons.Weapons,
                action["Target"] in self.get_alive_countries()
            ))
        except KeyError as e:
            print("KeyError", e)
            return False


    def _serialize_countries(self):
        countries = []
        for country in self.countries:
            countries.append(country.serialize())

        return countries

    def _run_actions(self, actions: List[dict]):
        self.events = []
        alive = self.get_alive_countries()

        for action in actions:
            if "Weapon" in action and action["Weapon"] in weapons.Weapons:
                self.events.append(action)

                if action["Success"]:
                    damage = action["Weapon"].value.DAMAGE
                    self.countries[action["Target"]].take_damage(damage)


        # Kill players who died this turn
        for player in alive:
            if self.countries[player].health == 0:
                self.countries[player].alive = False
                self.events.append({
                    "Weapon": "Death",
                    "Source": player
                })


def get_bots():
    # Dynamically import bots in bots directory to BOTS dictionary
    BOTS = {}  # A dictionary of bot names to Bot classes
    bots = os.path.join(abspath(dirname(dirname(__file__))), "bots")
    for file in os.listdir(bots):
        if not file.endswith(".py"):
            continue

        name = file.replace(".py", "")
        module = "." + name
        BOTS[name] = importlib.import_module(module, "bots").Bot

    return BOTS


def get_countries():
    BOTS = get_bots()

    countries = []
    for name in BOTS:
        bot_class = BOTS[name]
        current = country.Country(bot_class)
        current.name = name
        countries.append(current)

    return countries
