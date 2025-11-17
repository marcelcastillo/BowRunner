import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    full_path = BASE_IMG_PATH + path
    print("Trying to load:", full_path)
    img = pygame.image.load(BASE_IMG_PATH + path).convert() #Converts to pygame friendly representation
    img.set_colorkey((0, 0, 0))                             # Black becomes transparent
    return img

def load_images(path):
    # List of all our loaded images
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if not img_name.lower().endswith(".png"):
            continue
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    '''An Animation is a sequence of images rendered one after another'''
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

     