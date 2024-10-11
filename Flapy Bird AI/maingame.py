import pygame
import random
import neat  # Import NEAT directly
# Removed import neat_utils, as it's not needed here

# Game constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_WIDTH = 80
PIPE_GAP = 200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame and set up the screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load textures and assets after display initialization
bird_sprite_sheet = pygame.image.load("textures/Player/StyleBird2/Bird2-2.png").convert_alpha()
pipe_sprite = pygame.image.load("textures/Tiles/Style1/PipeStyle1.png").convert_alpha()
bg_img = pygame.image.load("textures/Background/Background5.png").convert_alpha()

# Resize assets
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pipe_sprite = pygame.transform.scale(pipe_sprite, (PIPE_WIDTH, 500))

# Load sprite frames
def load_sprite_frames(sheet, num_frames):
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // num_frames
    frame_height = sheet_height
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

# Bird and pipe animation frames
BIRD_FRAME_COUNT = 4
PIPE_FRAME_COUNT = 1
bird_frames = load_sprite_frames(bird_sprite_sheet, BIRD_FRAME_COUNT)
pipe_frame = load_sprite_frames(pipe_sprite, PIPE_FRAME_COUNT)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animation_counter = 0
        self.score = 0
        self.alive = True
        self.image = pygame.image.load("textures/Player/StyleBird2/Bird2-2.png")
        self.width = self.image.get_width()  # Get the width of the texture
        self.height = self.image.get_height()

    def jump(self):
        self.velocity = self.lift

    def update(self):

        if self.alive:
            self.velocity += self.gravity
            self.y += self.velocity
            if self.y > SCREEN_HEIGHT - bird_frames[0].get_height():
                self.y = SCREEN_HEIGHT - bird_frames[0].get_height()
                self.velocity = 0
            if self.y < 0:
                self.y = 0
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.frame_index = (self.frame_index + 1) % BIRD_FRAME_COUNT
                self.animation_counter = 0
            if self.y > 700 or self.y < 0:  # Check if bird goes off-screen
                self.alive = False  # Bird dies if it goes off-screen
    

    def draw(self, screen):
        screen.blit(bird_frames[self.frame_index], (self.x, self.y))

    def get_state(self, pipes):
        pipe = pipes[0] if pipes else (SCREEN_WIDTH, 0)
        pipe_dist = pipe[0] - self.x
        pipe_top = pipe[1]
        pipe_bottom = pipe[1] + PIPE_GAP
        return [self.y, self.velocity, pipe_dist, pipe_top, pipe_bottom]
    def check_collision(self, pipes):
        for pipe in pipes:
            # Check for collision between bird and pipes (you should implement the logic)
            if self.x + self.width > pipe.x and self.x < pipe.x + pipe.width:
                if self.y + self.height > pipe.height or self.y < pipe.height - Pipe.PIPE_GAP:
                    self.alive = False  # Bird dies if it collides with a pipe
 
    def collide_with_pipes(self, pipes):
        # Check if the bird collides with any of the pipes
        bird_rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Bird's bounding rectangle
        for pipe in pipes:
            pipe_rect_top = pygame.Rect(pipe.x, 0, pipe.width, pipe.height)  # Top pipe
            pipe_rect_bottom = pygame.Rect(pipe.x, pipe.height + PIPE_GAP, pipe.width, 700)  # Bottom pipe
            
            # If the bird collides with either the top or bottom pipe, return True
            if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
                return True
        
        return False  # No collision detected
class Pipe:

    
    def __init__(self):

        self.x = SCREEN_WIDTH
        self.width = PIPE_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= 5

    def draw(self, screen):
        top_pipe = pygame.transform.flip(pipe_sprite, False, True)
        screen.blit(top_pipe, (self.x, self.height - top_pipe.get_height()))
        screen.blit(pipe_sprite, (self.x, self.height + PIPE_GAP))

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, bird_frames[0].get_width(), bird_frames[0].get_height())
        top_pipe_rect = pygame.Rect(self.x, self.height - pipe_sprite.get_height(), PIPE_WIDTH, pipe_sprite.get_height())
        bottom_pipe_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, pipe_sprite.get_height())
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

def run_game(net):
    bird = Bird()
    pipes = [Pipe()]
    pipe_counter = 0
    score = 0
    running = True
    fitness = 0

    while running:
        state = bird.get_state(pipes)
        output = net.activate(state)

        if output[0] > 0.5:
            bird.jump()

        bird.update()
        pipe_counter += 5

        if pipe_counter >= 300:
            pipes.append(Pipe())
            pipe_counter = 0

        for pipe in pipes:
            pipe.update()
            if pipe.collide(bird):
                running = False

            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe())
                score += 1

        fitness = score

    return fitness

def eval_genomes(genomes, config):
    # Move this import inside the function to avoid circular imports
    from neat_utils import eval_genomes
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        fitness = run_game(net)
        genome.fitness = fitness

if __name__ == "__main__":
    config_path = "config/config-feedforward.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.Checkpointer(5))
    winner = population.run(eval_genomes, 50)
    print("Best genome:\n", winner)
