#!/usr/bin/python3

from typing import List
from bots import sample_bot
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


    def action(self, world_state):
        # Format action before appending
        country_status = self.serialize()

        action = self.player.action(country_status, world_state)
        return action


    def serialize(self):
        country_status = {
            "Alive": self.alive,
            "Health": self.health,
            "Resources": self.resources,
            "Nukes": self.nukes
        }

        return country_status


    def take_damage(self, damage):
        self.health -= damage

        if self.health < 0:
            self.alive = False


class Game:
    MAX_TURNS = 100

    def __init__(self, countries: List[Country]):
        self.countries = countries
        # Initialize ids
        for i, country in enumerate(self.countries):
            country.id = i

        self.turn = 1


    def start(self):
        while (self._get_alive_count() > 1
               and self.turn <= self.MAX_TURNS):

            actions = self._get_actions()
            self._run_actions(actions)
            self.turn += 1


    def _get_alive_count(self):
        """ Returns an integer """
        return sum(country.alive for country in self.countries)


    def _get_alive_countries(self):
        """ Returns indexes """
        return [pos for pos, country in enumerate(self.countries) if country.alive]


    def _get_world_state(self):
        return {
            "countries": self._serialize_countries(),
            "player_count": self._get_alive_count()
        }


    def _get_actions(self):
        actions = []
        world_state = self._get_world_state()

        for i, country in enumerate(self.countries):
            if not country.alive:
                continue

            action = country.action(world_state)

            # Check if action is valid
            # If action is invalid, nuke own country
            if not self._is_valid_action(action):
                action = {
                    "Weapon": "Wait"
                }

            actions.append(action)

        return actions


    def _is_valid_action(self, action):
        return all(
            "Target" in action,
            "Weapon" in action,
            action["Weapon"] in weapons.Weapons,
            action["Target"] in self._get_alive_countries()
        )


    def _serialize_countries(self):
        countries = []
        for country in self.countries:
            countries.append(country.serialize())

        return countries

    def _run_actions(self, actions):
        for action in actions:
            if action["Weapon"] != "Wait":
                continue

            if action["Weapon"] == 1:  # LASER
                pass

            elif action["Weapon"] == 2:  # Missile
                pass

            elif action["Weapon"] == 3:  # Nuke
                pass

    def _nuke_country(self, target):
        pass



def main():
    countries = []
    for _ in range(10):
        countries.append(Country(sample_bot.Bot()))

    active_game = Game(countries)
    active_game.start()


if __name__ == "__main__":
    main()
