from visualizer.country import Country


import math


TAU = math.pi * 2


class Countries:
    def __init__(self, game_countries, SIZE):
        WIDTH, HEIGHT = SIZE

        self.all = []
        country_count = len(game_countries)

        for i, c in enumerate(game_countries):
            perc = (math.sin(i * TAU / country_count) / 2 + 1/2)
            x = (0.1 + 0.8 * perc) * WIDTH

            perc = (math.cos(i * TAU / country_count) / 2 + 1/2)
            y = (0.15 + 0.75 * perc) * HEIGHT

            self.all.append(Country(c, (x, y)))

    def draw(self, window):
        # Draw countries
        dirty_rects = []

        for c in self.all:
            dirty_rects += c.draw(window)

        return dirty_rects

    def get_pos(self, i):
        return self.all[i].border.center

    def resize(self, WIDTH, HEIGHT):
        country_count = len(self.all)

        for i, c in enumerate(self.all):
            perc = (math.sin(i * TAU / country_count) / 2 + 1/2)
            x = (0.1 + 0.8 * perc) * WIDTH

            perc = (math.cos(i * TAU / country_count) / 2 + 1/2)
            y = (0.15 + 0.75 * perc) * HEIGHT

            c.set_pos((x, y))
