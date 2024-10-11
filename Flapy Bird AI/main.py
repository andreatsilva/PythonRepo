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

""""WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)"""



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
BIRD_FRAME_COUNT = 4

bird_sprite_sheet = pygame.image.load("textures/Player/StyleBird2/Bird2-2.png").convert_alpha()
pipe_sprite = pygame.image.load("textures/Tiles/Style1/PipeStyle1.png").convert_alpha()
bg_img = pygame.image.load("textures/Background/Background5.png").convert_alpha()

bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pipe_sprite = pygame.transform.scale(pipe_sprite, (PIPE_WIDTH, 500))

#load the sprites

def load_sprite_frames(sheet, num_frames):
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // num_frames  # Divide total width by the number of frames
    frame_height = sheet_height  # Use the full height of the sprite sheet
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

# Now use this corrected function
bird_frames = load_sprite_frames(bird_sprite_sheet, BIRD_FRAME_COUNT)


class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10
        self.frame_index = 0  # Current animation frame index
        self.animation_speed = 0.1  # Control how fast frames change
        self.animation_counter = 0  # Counts time to switch frames
        self.score = 0 

    def jump(self):
        self.velocity = self.lift

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # Prevent bird from falling off the screen
        if self.y > SCREEN_HEIGHT - bird_frames[0].get_height():
            self.y = SCREEN_HEIGHT - bird_frames[0].get_height()
            self.velocity = 0
        if self.y < 0:
            self.y = 0

        # Animation logic
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.frame_index = (self.frame_index + 1) % BIRD_FRAME_COUNT
            self.animation_counter = 0

    def draw(self, screen):
        screen.blit(bird_frames[self.frame_index], (self.x, self.y))

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= 5

    def draw(self, screen):
        # Draw top pipe (rotated 180 degrees)
        top_pipe = pygame.transform.flip(pipe_sprite, False, True)
        screen.blit(top_pipe, (self.x, self.height - top_pipe.get_height()))
        
        # Draw bottom pipe
        screen.blit(pipe_sprite, (self.x, self.height + PIPE_GAP))

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, bird_frames[0].get_width(), bird_frames[0].get_height())
        top_pipe_rect = pygame.Rect(self.x, self.height - pipe_sprite.get_height(), PIPE_WIDTH, pipe_sprite.get_height())
        bottom_pipe_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, pipe_sprite.get_height())

        # Check if bird collides with any pipe
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True

    while running:
        screen.blit(bg_img, (0, 0))  # Draw background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update Bird
        bird.update()

        # Update Pipes
        for pipe in pipes:
            pipe.update()

            # Check for collision
            if pipe.collide(bird):
                running = False

            # Add new pipes
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe())
                bird.score += 1

        # Draw Bird
        bird.draw(screen)

        # Draw Pipes
        for pipe in pipes:
            pipe.draw(screen)

        # Update screen
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()