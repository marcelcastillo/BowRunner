import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Bowrunner')     

        self.screen = pygame.display.set_mode((640, 480))   # Creates the window (resolution in pixels)
        self.display = pygame.Surface((320, 240))           # Half the resulution of the screen and then project this onto screen for pixel art effect
    
        self.clock = pygame.time.Clock()                    # Initialize clock

        self.movement = [False, False]                      # Boolean determining [left, right] movement

        # Asset map
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png')
        }
        print(self.assets)

        # Player Object Entity
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

    def run(self):
        while True:
            self.display.fill((14, 219, 248))            # Rerenders the screen with a blue/green hue

            # Key a pressed -> self.movement[0] = True(1)
            # Key d pressed -> self.movement[1] = True(1)
            self.player.update((-1*self.movement[0] + self.movement[1], 0))
            self.player.render(self.display)
            
            for event in pygame.event.get():            # Gets user input
                if event.type == pygame.QUIT:               # User clicks the x on the window
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0, 0))
            pygame.display.update()                     
            self.clock.tick(60)                              # Forces loop to run at 60 FPS

Game().run()