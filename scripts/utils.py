import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() #Converts to pygame friendly representation
    img.set_colorkey((0, 0, 0))                             # Black becomes transparent
    return img

def load_images(path):
    # List of all our loaded images
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images