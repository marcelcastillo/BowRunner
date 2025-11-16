# Responsible for

import pygame

class PhysicsEntity:
    '''Currently the player characterized by pos (coords), size, and velocity'''
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)                    # Movement logic: img_pos[1] is the y-coord
        self.size = size
        self.velocity = [0.0, 0.0]
    
    def rect(self):
        '''Player "hitbox" '''
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, tilemap, movement=(0, 0)):
        '''Update the player's location based on user input'''
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])     

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()   
        # Loop through the 9 tiles around the player
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # Modify the player entity hitbox
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()   
        # Loop through the 9 tiles around the player
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # Modify the player entity hitbox
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        # Gravity always affects the player entity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Reset player velocity upon collision
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0


    def render(self, surf, offset=(0, 0)):
        '''Renders the player sprite onto the display surface'''
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))