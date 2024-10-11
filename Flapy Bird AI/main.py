##Flapy Bird Game that uses AI 


import pygame
import random



pygame.init()

#game cons
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
BIRD_WIDTH = 50
BIRD_HEIGH = 50
PIPE_WIDTH = 80
PIPE_HEIGHT = 80
PIPE_GAP  = 200 


#colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.clock()

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10
        self.score = 0

    def jump(self):
        self.velocity = self.lift

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y > SCREEN_HEIGHT - BIRD_HEIGH:
            self.y = SCREEN_HEIGHT - BIRD_HEIGH
            self.velocity = 0
        if self.y < 0:
            self.y = 0

    def draw (self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, BIRD_WIDTH, BIRD_HEIGH))

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 100)
        self.passed = False

        def update(self):
            self.x -= 5

        def draw(self, screen):
            pygame.draw.rect(screen, BLACK, ( self.x, 0, PIPE_WIDTH, self.height))
            pygame.draw.rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)
        def collide(self, bird)
