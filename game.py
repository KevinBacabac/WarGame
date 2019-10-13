#!/usr/bin/python3

import time

from resources import weapons
from resources.game_logic import GameLogic


class TextGame:
    def __init__(self):
        self.game = GameLogic()

    def start(self):
        while (self.game.get_alive_count() > 1
               and self.game.turn <= self.game.MAX_TURNS):

            self.game.do_turn()
            self._print_events()

        if self.game.get_alive_count() == 1:
            alive = self.game.get_alive_countries()[0]
            print(self.game.countries[alive].name, "is the last one standing.")

        else:
            print("There were no survivors.")

        print("Hit enter to exit.")
        input()


    def _print_events(self):
        def name(id):
            return self.game.countries[id].name

        for event in self.game.events:
            source = name(event["Source"])

            if "Target" in event:
                target = name(event["Target"])
            else:
                target = None

            if "Weapon" not in event:
                if target:
                    print(source, "decided to wait and stared at", target)
                else:
                    print(source, "decided to wait.")

            elif event["Weapon"] == weapons.Weapons.LASER:  # LASER
                print(source, "fired a laser at", target)

            elif event["Weapon"] == weapons.Weapons.MISSILE:  # Missile
                print(source, "fired a missile at", target)

            elif event["Weapon"] == weapons.Weapons.NUKE:
                print(source, "fired a nuke at", target)

                if not event["Success"]:
                    print("But they ran out of nukes.")

            elif event["Weapon"] == "Death":
                print(source, "is dead!")

        time.sleep(1)


if __name__ == "__main__":
    active_game = TextGame()
    active_game.start()
