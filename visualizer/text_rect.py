class TextRect:
    __slots__ = ("dirty_rects", "font", "last_text", "text", "foreColour",
                 "rect", "surface")

    def __init__(self, font, text: str, foreColour):
        self.font = font

        self.last_text = None
        self.text = text

        self.foreColour = foreColour

        self.dirty_rects = []
        self.rect = None
        self.check_update()

    def check_update(self):
        if self.text != self.last_text:
            # Antialias is True
            self.surface = self.font.render(self.text, True, self.foreColour)
            self.last_text = self.text
            self.realign_rect()

    def draw(self, window):
        self.check_update()
        window.blit(self.surface, self.rect)

        temp = self.dirty_rects.copy()
        self.dirty_rects = []
        return temp

    def realign_rect(self):
        if not self.rect:
            self.rect = self.surface.get_rect()

        self.dirty_rects.append(self.rect.copy())
        self.dirty_rects.append(self.rect)

        old_center = self.rect.center

        self.rect.size = self.surface.get_size()
        self.rect.center = old_center
