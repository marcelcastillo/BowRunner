import sys
import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('editor')     

        self.screen = pygame.display.set_mode((640, 480))   # Creates the window (resolution in pixels)
        self.display = pygame.Surface((320, 240))           # Half the resulution of the screen and then project this onto screen for pixel art effect
        self.clock = pygame.time.Clock()                    # Initialize clock

        # Asset map
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone')
        }

        # Moving the editor around
        self.movement = [False, False, False, False]                      

        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.scroll = [0.0, 0.0]    # The game "camera". Provides an offset that shifts the render location of every asset in the game

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        # Control group for tile selection
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.on_grid = True

    def run(self):
        while True:
            # Initialize with black screen
            self.display.fill((0, 0, 0))   

            # Reposition camera
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Render the tilemap onto the display
            self.tilemap.render(self.display, offset=render_scroll)

            # Turn the asset dictionary into a list that we can loop through with user input
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            # Returns pixel coords of mouse with respect to the window
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1]/RENDER_SCALE)

            # Adjust the tile position based on the current window scroll 
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.on_grid:
                # Render the selected tile to be placed
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            # Take user input and add it to the tilemap
            if self.clicking and self.on_grid:
                self.tilemap.tilemap[(tile_pos[0], tile_pos[1])] = {'type': self.tile_list[self.tile_group],
                                                                              'variant': self.tile_variant,
                                                                              'pos': tile_pos}
            if self.right_clicking:
                tile_loc = (tile_pos[0], tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                
                for tile in self.tilemap.offgrid_tiles.copy():  # You're removing from this list and need to iterate on a copy
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                         tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)


            # Render the currently selected tile onto the screen
            self.display.blit(current_tile_img, (5, 5))
            
            # Capture user input
            for event in pygame.event.get():            # Gets user input
                if event.type == pygame.QUIT:               # User clicks the x on the window
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.on_grid:
                            self.tilemap.offgrid_tiles.append( {'type': self.tile_list[self.tile_group],
                                                                'variant': self.tile_variant,
                                                                'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    
                    # Indexing through the asset lists
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]]) 
                    else:
                        if event.button == 4:
                            self.tile_group = (self .tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)    
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False                
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            # Images are rendered to display but are then projected and scaled onto the screen
            # This magnifies the pixel art effect
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0, 0))
            pygame.display.update()                     
            self.clock.tick(60)                              # Forces loop to run at 60 FPS

Editor().run()