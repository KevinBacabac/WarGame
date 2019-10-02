#!/usr/bin/python3

from typing import List
from bots import sample_bot
from resources import weapons
import time

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
        action["ID"] = self.id
        return action


    def serialize(self):
        country_status = {
            "Alive": self.alive,
            "Health": self.health,
            "ID": self.id,
            "Resources": self.resources,
            "Nukes": self.nukes
        }

        return country_status


    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.health = 0

        else:
            pass  # print(self.id, "HP is", self.health)


class Game:
    MAX_TURNS = 30

    def __init__(self, countries: List[Country]):
        self.countries = countries
        self.events = []

        # Initialize ids
        for i, country in enumerate(self.countries):
            country.id = i

        self.turn = 1


    def start(self):
        while (self._get_alive_count() > 1
               and self.turn <= self.MAX_TURNS):

            print("Round", self.turn)
            actions = self._get_actions()
            self._run_actions(actions)
            self._print_events()
            self.turn += 1

        if self._get_alive_count() == 1:
            alive = self._get_alive_countries()[0]
            print(alive, "is the last one standing.")

        else:
            print("There were no survivors.")


    def _get_alive_count(self):
        """ Returns an integer """
        return sum(country.alive for country in self.countries)


    def _get_alive_countries(self):
        """ Returns indexes """
        return [pos for pos, country in enumerate(self.countries) if country.alive]


    def _get_world_state(self):
        return {
            "countries": self._serialize_countries(),
            "events": self.events,
            "alive_players": self._get_alive_countries()
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
                    "Action": "Wait"
                }

            actions.append(action)

        return actions


    def _is_valid_action(self, action):
        try:
            return all((
                weapons.Weapons.has(action["Action"]),
                action["Target"] in self._get_alive_countries()
            ))
        except KeyError:
            print("KeyError", action)
            return False


    def _serialize_countries(self):
        countries = []
        for country in self.countries:
            countries.append(country.serialize())

        return countries

    def _run_actions(self, actions):
        self.events = []
        alive = self._get_alive_countries()

        for action in actions:
            if action["Action"] == 0:
                self.events.append(action)

            elif action["Action"] == 1:  # LASER
                self.events.append(action)
                self.countries[action["Target"]].take_damage(20)

            elif action["Action"] == 2:  # Missile
                self.events.append(action)
                self.countries[action["Target"]].take_damage(20)

            elif action["Action"] == 3:  # Nuke
                action["Success"] = bool(self.countries[action["ID"]].nukes)
                self.events.append(action)

                if self.countries[action["ID"]].nukes:
                    self.countries[action["ID"]].nukes -= 1

                    self.countries[action["Target"]].take_damage(100)


        # Kill players who died this turn
        for player in alive:
            if self.countries[player].health == 0:
                self.countries[player].alive = False
                self.events.append({
                    "Action": "Death",
                    "ID": player
                })

    def _print_events(self):
        for event in self.events:
            if event["Action"] == 0:
                print(event["ID"], "decided to wait.")

            elif event["Action"] == 1:  # LASER
                print(event["ID"], "fired a laser at", event["Target"])

            elif event["Action"] == 2:  # Missile
                print(event["ID"], "fired a missile at", event["Target"])

            elif event["Action"] == 3:
                print(event["ID"], "fired a nuke at", event["Target"])
                if not event["Success"]:
                    print("But they ran out of nukes.")

            elif event["Action"] == "Death":
                print(event["ID"], "is dead!")

        time.sleep(1)



def main():
    countries = []
    for _ in range(6):
        countries.append(Country(sample_bot.Bot()))

    active_game = Game(countries)
    active_game.start()


if __name__ == "__main__":
    main()
