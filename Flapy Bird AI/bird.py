import pygame

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10

    def jump(self):
        self.velocity = self.lift

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self, screen, frames, frame_index):
        screen.blit(frames[frame_index], (self.x, self.y))

    def is_off_screen(self, screen_height):
        return self.y < 0 or self.y > screen_height
    
