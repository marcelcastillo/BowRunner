import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Bowrunner')        
        self.screen = pygame.display.set_mode((640, 480))    # Creates the window (resolution in pixels)

        self.clock = pygame.time.Clock()                     # Initialize clock
        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        self.img.set_colorkey((0, 0, 0))

        self.img_pos = [160, 260]           # [x-coord, y-coord(neg)] Origin (0, 0) is top-left corner of screen
        self.movement = [False, False]

        self.collision_area = pygame.Rect(50, 50, 300, 50)

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))            # Rerenders the screen with a blue/green hue


            # Movement logic: img_pos[1] is the y-coord
            # 
            self.img_pos[1] += (-1*self.movement[0] + self.movement[1]) * 5

            self.screen.blit(self.img, self.img_pos)

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            
            for event in pygame.event.get():            # Gets user input
                if event.type == pygame.QUIT:               # User clicks the x on the window
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.movement[0] = True
                    if event.key == pygame.K_s:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement[0] = False
                    if event.key == pygame.K_s:
                        self.movement[1] = False

            pygame.display.update()                     
            self.clock.tick(60)                              # Forces loop to run at 60 FPS

Game().run()