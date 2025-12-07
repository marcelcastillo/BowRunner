import json
import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
AUTOTILE_TYPES = {'grass', 'stone'}
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:   
    '''The game "world". The set of tiles and grid locations that comprises the level.''' 
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        # Square grid of our tiles
        self.tilemap = {}
        self.offgrid_tiles = [] # A list of dictionaries

        # A simple horizontal platform of grass
        # for i in range(10):
        #     # These are grid coordinates, not pixel locations
        #     self.tilemap[(3 + i, 10)] = { # Contents of 'tile' var in render
        #                                 'type': 'grass', 
        #                                 'variant': 1,
        #                                 'pos': (3 + i, 10)
        #                                 }
        self.load('map.json')
    
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

    def save(self, path):
        '''Create a JSON representation of the tilemap dictionary of our level'''
        serializable = {
            'tilemap': { f"{x};{y}": data for (x, y), data in self.tilemap.items() },
            'tile_size': self.tile_size,
            'offgrid': self.offgrid_tiles
            }
        with open(path, 'w') as f:
            json.dump(serializable, f, indent=4)
            f = open(path, 'w')
            f.close()
    
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        tilemap = {}
        for key, data in map_data['tilemap'].items():
            x, y = map(int, key.split(';'))
            data['pos'] = tuple(data['pos'])
            tilemap[(x, y)] = data

        self.tilemap = tilemap
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc] # (x, y)
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = (tile['pos'][0] + shift[0], tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]


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

        