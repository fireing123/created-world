import pygame
import math

class Vector(pygame.Vector2):
    
    def floor_vector(self):
        return Vector(
            math.floor(self.x), 
            math.floor(self.y)
        )