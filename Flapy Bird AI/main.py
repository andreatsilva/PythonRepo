import neat
import pygame
from maingame import Bird, Pipe  # Import Bird and Pipe
from neat_utils import eval_genomes

config_path = "config/config-feedforward.txt" 
# Running the NEAT algorithm
def run_neat(config_path):
    # Load configuration file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create a population
    population = neat.Population(config)

    # Add a reporter to show progress in the terminal
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.Checkpointer(5))  # Save checkpoint every 5 generations

    # Run the NEAT algorithm with eval_genomes
    winner = population.run(lambda genomes, config: eval_genomes(genomes, config), 50)  # 50 generations


if __name__ == "__main__":
    run_neat('config/config-feedforward.txt')  # Pass the config file for NEAT

