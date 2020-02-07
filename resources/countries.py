from os.path import abspath, dirname
from typing import Dict, List
from random import shuffle

import importlib
import os

from resources.country import Country
from resources import helpers


class Countries:
    __slots__ = 'countries',

    def __init__(self):
        BOTS = get_bots()

        self.countries = []

        order = list(BOTS.keys())
        shuffle(order)

        for i, filename in enumerate(order):
            bot_class = BOTS[filename]
            current = Country(bot_class)
            current.filename = filename
            current.name = filename.replace("_", " ").title()
            current.id = i
            self.countries.append(current)

    def check_deaths(self, alive_players: List):
        death_events = []

        # Kill players who died this turn
        for player in alive_players:
            if self.countries[player].health == 0:
                event = self.countries[player].killer
                source = event["Source"]
                self.countries[player].alive = False

                death_events.append(event)

                self.countries[source].kills.append(player)
                self.countries[source].nukes += 1
                self.countries[source].nukes += self.countries[player].nukes
                self.countries[player].nukes = 0

        return death_events

    def get_actions(self, world_state: Dict):
        actions = []

        for i, country in enumerate(self.countries):
            if not country.alive:
                continue

            action = country.get_action(world_state)

            # Prevent attacks on dead players so game has an end
            if (action  # Not idle
                    and action["Type"] == "Attack"
                    and self.get_alive_count() < 2
                    and action["Target"] not in self.get_alive()):
                continue

            actions.append(action)

        return actions

    def get_alive(self):
        """ Returns indices """
        return set([pos for pos, country in enumerate(self.countries) if country.alive])

    def get_alive_count(self):
        """ Returns an integer """
        return sum(country.alive for country in self.countries)

    def get_name(self, country_id: int):
        return self.countries[country_id].name

    def get_survivor(self):
        count = self.get_alive_count()

        if count == 0:
            return None
        if count == 1:
            alive = tuple(self.get_alive())[0]
            return self.countries[alive].name
        else:
            ids = self.get_alive()
            names = sorted([self.countries[i].name for i in ids])
            return ", ".join(names)

    def import_state(self, countries):
        lookup = {}
        for c in countries:
            lookup[c["ID"]] = c

        #for i in lookup:
        #    self.countries

    def serialize_countries(self):
        countries = []
        for country in self.countries:
            countries.append(country.serialize())

        return countries

    def __repr__(self):
        out = [self.countries[c].__repr__() for c in self.get_alive()]

        if out:
            return "\n".join(out)
        else:
            return "[]"


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
