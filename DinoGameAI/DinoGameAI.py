import numpy as np
import cv2
import win32gui
import mss
import mss.tools

import os
import neat
import visualize
import main as game
import globalVars as gv
import time

def eval_genomes(genomes, config):
    population = game.Dino_Pop(int(len(genomes)), 44, 47)
    nets = []
    

    for genome_id, genome in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
    
    #zippedList = zip(population.indivs, genomes, nets)
    gameInstance = game.mult_dino_gameplay(population)
    output = []
    outputPrev = []
    for i in range(len(population.indivs)):
        output.append([0.0,0.0])
        outputPrev.append([0,0])
    
    while(gv.gameOver == False):
        for i in range(len(population.indivs)):
            if population.indivs[i].isDead == False:
                outputPrev[i] = output[i]
                #print(game.GetInputs(gameInstance))
                output[i] = nets[i].activate(game.GetInputs(gameInstance))
                #print(output[i])
                output[i][0] = int(round(output[i][0]))
                output[i][1] = int(round(output[i][1]))
                if output[i][0] == 1:
                    game.Dino_Jump(population.indivs[i])
                elif output[i][1] == 1:
                    game.Dino_Duck(population.indivs[i])
                elif output[i][1] == 0 and outputPrev[i][1] == 1:
                    game.Dino_End_Duck(population.indivs[i])
        gameInstance.loop()
    #print(len(genomes))
    i = 0
    for genome_id, genome in genomes:
        #print(population.indivs[i].score)
        genome.fitness = population.indivs[i].score
        i += 1
    

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-44')
    p.run(eval_genomes, 10)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-file')
    run(config_path)


#game.gameplay()