#!/usr/bin/python3

from typing import List
from bots import sampleBot

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
        # Check if action is valid
        # If action is invalid, nuke own country
        # Format action before appending
        country_status = {}
        return self.player.action(country_status, world_history)


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


    def _get_actions(self):
        actions = []

        for country in self.countries:
            if not country.alive:
                continue

            action = country.action(self.world_history)
            actions.append(action)

        return actions

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
