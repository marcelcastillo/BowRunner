import sys
import pygame

from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

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
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle_bow'), img_dur=6),   # Bow assets
            'player/run': Animation(load_images('entities/player/run_bow'), img_dur=5),
            'player/jump': Animation(load_images('entities/player/jump_bow')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        # Player Object Entity
        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0.0, 0.0]    # The game "camera". Provides an offset that shifts the render location of every asset in the game

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))          

            # Offset that drifts camera centered onto the player. 
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()

            self.clouds.render(self.display, offset=render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (-1*self.movement[0] + self.movement[1], 0))               # Key a pressed -> self.movement[0] = True(1)
                                                                                                        # Key d pressed -> self.movement[1] = True(1)   
            self.player.render(self.display, offset=render_scroll)

            #print(self.tilemap.physics_rects_around(self.player.pos))
            
            for event in pygame.event.get():            # Gets user input
                if event.type == pygame.QUIT:               # User clicks the x on the window
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            # Images are rendered to display but are then projected and scaled onto the screen
            # This magnifies the pixel art effect
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0, 0))
            pygame.display.update()                     
            self.clock.tick(60)                              # Forces loop to run at 60 FPS

Game().run()