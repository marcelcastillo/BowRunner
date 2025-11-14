# Responsible for

import pygame

class PhysicsEntity:
    # Accepts the game state as a 
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)                    # Movement logic: img_pos[1] is the y-coord
        self.velocity = [0, 0]
    
    def update(self, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)