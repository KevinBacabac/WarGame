#!/usr/bin/python3

from typing import List
from bots import sampleBot
from resources import weapons


class Country:
    DEFAULT_HEALTH = 100
    DEFAULT_RESOURCES = 100
    NUKE_STOCKPILE = 1

    def __init__(self, player):
        self.alive = True
        self.health = self.DEFAULT_HEALTH
        self.resources = self.DEFAULT_RESOURCES
        self.nukes = self.NUKE_STOCKPILE
        self.player = player


    def action(self, world_history):
        # Format action before appending
        country_status = {"Health": self.health,
                          "Resources": self.resources,
                          "Nukes": self.nukes}

        action = self.player.action(country_status, world_history)
        return action



    def take_damage(self, damage):
        self.health -= damage

        if self.health < 0:
            self.alive = False


class Game:
    MAX_TURNS = 100

    def __init__(self, countries: List[Country]):
        self.countries = countries
        self.world_history = {"player_count": self._get_alive_count()}
        self.turn = 1


    def start(self):
        while (self._get_alive_count() > 1
               and self.turn <= self.MAX_TURNS):

            actions = self._get_actions()
            self._run_actions(actions)
            self.turn += 1


    def _get_alive_count(self):
        return sum(country.alive for country in self.countries)


    def _get_alive_countries(self):
        return [i for i, c in enumerate(self.countries) if c.alive]


    def _get_actions(self):
        actions = []

        for i, country in enumerate(self.countries):
            if not country.alive:
                continue

            action = country.action(self.world_history)

            # Check if action is valid
            # If action is invalid, nuke own country
            if not self._is_valid_action(action):
                action = self._nuke_country(i)

            actions.append(action)

        return actions


    def _is_valid_action(self, action):
        valid = ("Target" in action
                 and assert "Weapon" in action
                 and action["Weapon"] in weapons.Weapons
                 and action["Target"] in self._get_alive_countries()
        )

        return valid


    def _nuke_country(i):
        return {
            "Weapon": weapons.Weapons.NUKE,
            "Target": i
        }


    def _run_actions(self, actions):
        pass


def main():
    countries = []
    for _ in range(10):
        countries.append(Country(sampleBot.Bot()))

    active_game = Game(countries)
    active_game.start()


if __name__ == "__main__":
    main()
