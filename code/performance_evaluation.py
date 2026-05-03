import matplotlib.pyplot as plt
import tracemalloc
import numpy as np

from genetic_algorithm import GeneticAlgorithm
from ant_colony_algorithm import AntColonyAlgorithm
from particle_swarm_algorithm import pso
from common_functions import FitnessToViolationNumber

import time

def Algorithm_Evaluation(algorithm_function):
    iterations = 20

    algorithmTimes = []
    memoryData = []
    timeX = np.arange(0, 20, 1)
    generationData = []

    # Warmup Algorithm Run
    algorithm_function()

    # Run Algorithm multiple times and record runtime + memory usage
    for i in range(iterations):
        start = time.perf_counter()

        algData = algorithm_function()

        end = time.perf_counter()


        tracemalloc.start()

        algorithm_function()
        current, peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        generationData.append(algData)

        algorithmTimes.append(end - start)
        memoryData.append(peak)

        print(peak, "Bytes")
        print(end - start)

    fig, ax = plt.subplots(2, 1)
    fig.suptitle('Overall Algorithm Runtimes and Memory Usage')
    ax[0].plot(timeX, algorithmTimes)
    ax[0].set_xlabel('Iteration')
    ax[0].set_ylabel('Runtime (seconds)')
    ax[0].set_title('Algorithm Runtimes')

    ax[1].plot(timeX, memoryData)
    ax[1].set_xlabel('Iteration')
    ax[1].set_ylabel('Memory Usage (bytes)')
    ax[1].set_title('Algorithm Memory Usage')

    averageBestFitness = Plot_Algorithm_Generation_Data(generationData)
    averageAlgorithmTimes = sum(algorithmTimes) / len(algorithmTimes)
    averageMemoryUsage = sum(memoryData) / len(memoryData)
    return (averageAlgorithmTimes, averageMemoryUsage, averageBestFitness)

def Plot_Algorithm_Generation_Data(generationData):
    averageBestFitness = 0
    fig1, ax1 = plt.subplots(4, 5)
    fig2, ax2 = plt.subplots(4, 5)

    fig1.suptitle('Generation Fitness Data')
    fig1.supxlabel('Generation')
    fig1.supylabel('Fitness')

    fig2.suptitle('Generation Constraint Violation Data')
    fig2.supxlabel('Generation')
    fig2.supylabel('Constraint Violations')

    for x in range(4):
        for y in range(5):
            index = x * 5 + y
            run = generationData[index]

            plt.figure(fig1)
            fitness = [gen.bestFitness for gen in run]
            averageBestFitness += max(fitness)
            xTime = np.arange(0, len(fitness), 1)
            ax1[x][y].plot(xTime, fitness, color='blue', label='Best Fitness so far')

            fitness = [gen.minFitness for gen in run]
            ax1[x][y].plot(xTime, fitness, color='red', label='Min Fitness')

            fitness = [gen.maxFitness for gen in run]
            ax1[x][y].plot(xTime, fitness, color='green', label='Max Fitness this gen')

            fitness = [gen.averageFitness for gen in run]
            ax1[x][y].plot(xTime, fitness, color='orange', label='Average Fitness')

            plt.figure(fig2)
            fitness = [FitnessToViolationNumber(gen.bestFitness) for gen in run]
            ax2[x][y].plot(xTime, fitness, color='blue', label='Lowest Violations overall')

            fitness = [FitnessToViolationNumber(gen.minFitness) for gen in run]
            ax2[x][y].plot(xTime, fitness, color='red', label='Highest Violations')

            fitness = [FitnessToViolationNumber(gen.maxFitness) for gen in run]
            ax2[x][y].plot(xTime, fitness, color='green', label='Lowest Violation this gen')

            fitness = [FitnessToViolationNumber(gen.averageFitness) for gen in run]
            ax2[x][y].plot(xTime, fitness, color='orange', label='Average Violations')


    plt.show()

    return averageBestFitness

# dat = Algorithm_Evaluation(pso)
# print(dat)

geneticAverages = Algorithm_Evaluation(GeneticAlgorithm)
antColonyAverages = Algorithm_Evaluation(AntColonyAlgorithm)
psoAverages = Algorithm_Evaluation(pso)

# Average Algorithm Times
plt.figure(1)
plt.title("Average Algorithm Times")
plt.xlabel('Algorithm')
plt.ylabel('Time (seconds)')
plt.bar(["Genetic Algorithm", "Ant Colony Algorithm", "Particle Swarm Optimisation"],
        [geneticAverages[0], antColonyAverages[0], psoAverages[0]])

# Average Memory Usage
plt.figure(2)
plt.title("Average Memory Usage")
plt.xlabel('Algorithm')
plt.ylabel('Memory Usage (bytes)')
plt.bar(["Genetic Algorithm", "Ant Colony Algorithm", "Particle Swarm Optimisation"],
        [geneticAverages[1], antColonyAverages[1], psoAverages[1]])

# Average Best Fitness
plt.figure(3)
plt.title("Average Best Fitness")
plt.xlabel('Algorithm')
plt.ylabel('Fitness')
plt.bar(["Genetic Algorithm", "Ant Colony Algorithm", "Particle Swarm Optimisation"],
        [geneticAverages[2], antColonyAverages[2], psoAverages[2]])

plt.show()

