#!/usr/bin/python3

from typing import List


class Country:
    DEFAULT_HEALTH = 100
    DEFAULT_RESOURCES = 100
    NUKE_STOCKPILE = 1

    def __init__(self, player):
        self.alive = True
        self.health = self.DEFAULT_HEALTH
        self.resources = self.DEFAULT_RESOURCES
        self.nukes = 1
        self.player = player


    def action(self):
        # Check if action is valid
        # If action is invalid, nuke own country
        # Format action before appending
        pass


    def take_damage(self, damage):
        self.health -= damage

        if self.health < 0:
            self.alive = False


class Game:
    MAX_TURNS = 100

    def __init__(self, countries: List[Country]):
        self.countries = countries
        self.turn = 1


    def start(self):
        while (sum(country.alive for country in self.countries) > 1
               and self.turn <= self.MAX_TURNS):
            actions = self._get_actions()
            self._run_actions(actions)



    def _get_actions(self):
        actions = []
        for country in self.countries:
            if not country.alive:
                continue

            action = country.action()
            actions.append(action)

        return actions

    def _run_actions(self, actions):
        pass

def main():
    pass


if __name__ == "__main__":
    main()
