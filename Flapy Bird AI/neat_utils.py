import pygame
import neat
from maingame import Bird, Pipe  # Assuming you have Bird and Pipe from your game logic
import time

PIPE_GAP = 200  # Define PIPE_GAP here if not imported from maingame
PIPE_WIDTH = 80
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
BIRD_SPAWN_INTERVAL = 1  # 1 second between each bird spawn
PIPE_SPAWN_DISTANCE = 200  # Distance at which pipes spawn (adjust to your preference)
PIPE_WIDTH = 50  # Width of the pipes (or adjust as necessary)
PIPE_GAP = 200

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game_score = run_game_with_genome(genomes, config, num_birds=20)  # Using 20 birds per try
        genome.fitness = game_score
def run_game_with_genome(genomes, config, num_birds=20):
    # Create birds and associate each bird with a genome
    birds = [Bird() for _ in range(num_birds)]
    nets = [neat.nn.FeedForwardNetwork.create(genome, config) for _, genome in genomes]  # Create network for each bird
    pipes = [Pipe()]
    score = 0
    pipe_counter = 0
    running = True
    clock = pygame.time.Clock()

    # Initialize Pygame
    screen = pygame.display.set_mode((500, 700))
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Update each bird
        for bird, net, genome in zip(birds, nets, genomes):
            # Get inputs for the neural network
            pipe_mid_y = pipes[0].height + PIPE_GAP / 2
            inputs = [
                bird.y / 700,
                bird.velocity / 10,
                (pipes[0].x - bird.x) / 500,
                (pipe_mid_y - bird.y) / 700,
                bird.y / 700
            ]

            # Neural network output decides if the bird should jump
            output = net.activate(inputs)
            if output[0] > 0.5:
                bird.jump()

            bird.update()

        # Pipe spawning logic
        pipe_counter += 5
        if pipe_counter >= PIPE_SPAWN_DISTANCE:
            pipes.append(Pipe())
            pipe_counter = 0

        # Draw birds and pipes
        for bird in birds:
            bird.draw(screen)
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

        # Check for collisions for each bird
        for bird, genome in zip(birds, genomes[:]):
            if bird.y >= 700 or bird.y <= 0 or any(pipe.collide(bird) for pipe in pipes):
                birds.remove(bird)
                genomes.remove(genome)  # Remove genome if bird dies

        # Remove pipes that have gone off-screen
        for pipe in pipes[:]:
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                score += 1

        # If all birds are dead, stop the game
        if not birds:
            running = False

        # Draw the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Cap frame rate
        clock.tick(30)

        # Update the display
        pygame.display.update()

    return score
