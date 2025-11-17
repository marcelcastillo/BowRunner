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
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
    
    def rect(self):
        '''Player "hitbox" '''
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.e_type + '/' + self.action].copy()
    
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

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        # Gravity always affects the player entity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Reset player velocity upon collision
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()


    def render(self, surf, offset=(0, 0)):
        '''Renders the player sprite onto the display surface'''
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], 
                                                                                  self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')