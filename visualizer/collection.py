class Collection:
    class_type = None

    def __init__(self):
        self.all = []

    def add(self, *args):
        self.all.append(self.class_type(*args))
