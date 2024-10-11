import pygame

class Pipe:
    PIPE_WIDTH = 50
    PIPE_HEIGHT = 300

    def __init__(self, x, height, gap_size=150):
        self.x = x
        self.height = height
        self.gap_size = gap_size
        self.top = pygame.Rect(self.x, 0, self.PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, self.height + self.gap_size, self.PIPE_WIDTH, Pipe.PIPE_HEIGHT)

    def move(self, speed):
        self.x -= speed
        self.top.x = self.x
        self.bottom.x = self.x

    def draw(self, screen, pipe_top_image, pipe_bottom_image):
        screen.blit(pipe_top_image, (self.x, self.top.y))
        screen.blit(pipe_bottom_image, (self.x, self.bottom.y))

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, bird.frames[0].get_width(), bird.frames[0].get_height())
        return bird_rect.colliderect(self.top) or bird_rect.colliderect(self.bottom)