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
clock = pygame.time.Clock()

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
        pygame.draw.rect(screen, BLACK, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.height + PIPE_GAP)))
    def collide(self, bird):
        if bird.y < self.height or bird.y + BIRD_HEIGH > self.height + PIPE_GAP:
            if self.x < bird.x + BIRD_WIDTH < self.x + PIPE_WIDTH:
                return True
            return False
            
def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()


        for pipe in pipes:

            pipe.update()

            if pipe.collide(bird):
                running = False

            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe())
                bird.score += 1


        bird.draw(screen)

        for pipe in pipes:
            pipe.draw(screen)

        pygame.display.update()
        clock.tick(30)
    pygame.quit()
if __name__ == "__main__":
    main()