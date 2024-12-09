from pygameHelper import GameObject

class Particle(GameObject):
    def __init__(self, name, position):
        super().__init__(name, 2, "particle", True, position, 0, "parent")