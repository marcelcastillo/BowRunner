import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:   
    '''The game "world". The set of tiles and grid locations that comprises the level.''' 
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        # Square grid of our tiles
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            # These are grid coordinates, not pixel locations
            self.tilemap[(3 + i, 10)] = { # Contents of 'tile' var in render
                                        'type': 'grass', 
                                        'variant': 1,
                                        'pos': (3 + i, 10)
                                        }
            self.tilemap[(10, i + 5)] = {
                                        'type': 'stone', 
                                        'variant': 1,
                                        'pos': (10, 5 + i)
                                        }
    
    def tiles_around(self, pos):
        """Compute the tiles in the 3x3 "square around the player"""
        tiles = []
        # Convert pixel position into grid position
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

        for offset in NEIGHBOR_OFFSETS:
            check_loc = tile_loc[0] + offset[0], tile_loc[1] + offset[1]
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
    
        return tiles

    def physics_rects_around(self, pos):
        '''Compute the "physics enabled" tiles around the player'''
        # We only want to compute physics for tiles close to the player's position
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                # Create the rectangle around the tile
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects


    def render(self, surf, offset=(0, 0)):
        '''Renders the tiles defined in the tilemap'''
        # Render the offgrid tiles
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # Render the on-grid tiles
        # For a given camera offset, get the tilemap grids that are visible to the display surface
        # Transform pixel location to tile coordinate
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = (x, y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], 
                        (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))




        # # Render the on-grid tiles
        # for loc in self.tilemap:
        #     tile = self.tilemap[loc]
        #     # Render the tile:           
        #     # Get the type and variant specified in the tilemap above from the game assets
        #         # Blit it to the screen at the position specified above
        #     surf.blit(self.game.assets[tile['type']][tile['variant']], 
        #                 (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        