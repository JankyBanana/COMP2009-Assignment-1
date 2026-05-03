import matplotlib.pyplot as plt
import tracemalloc
import numpy as np

from genetic_algorithm import GeneticAlgorithm
from ant_colony_algorithm import AntColonyAlgorithm
from particle_swarm_algorithm import pso

import time


def Algorithm_Evaluation(algorithm_function):
    iterations = 20

    algorithmTimes = []
    memoryData = []
    timeX = np.arange(0, 20, 1)
    generationData = []


    for i in range(iterations):
        start = time.perf_counter()
        tracemalloc.start()

        generationData.append(algorithm_function())

        end = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        algorithmTimes.append(end - start)
        memoryData.append(peak)

        print(peak, "Bytes")
        print(end - start)

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(timeX, algorithmTimes)
    ax[1].plot(timeX, memoryData)

    averageBestFitness = Plot_Algorithm_Generation_Data(generationData)
    averageAlgorithmTimes = sum(algorithmTimes) / len(algorithmTimes)
    averageMemoryUsage = sum(memoryData) / len(memoryData)
    return (averageAlgorithmTimes, averageMemoryUsage, averageBestFitness)

def Plot_Algorithm_Generation_Data(generationData):
    averageBestFitness = 0
    fig, ax = plt.subplots(4, 5)
    for x in range(4):
        for y in range(5):
            index = x * 5 + y
            run = generationData[index]

            fitness = [gen.bestFitness for gen in run]
            averageBestFitness += max(fitness)
            xTime = np.arange(0, len(fitness), 1)
            ax[x][y].plot(xTime, fitness, color='blue')

            fitness = [gen.minFitness for gen in run]
            ax[x][y].plot(xTime, fitness, color='red')

            fitness = [gen.maxFitness for gen in run]
            ax[x][y].plot(xTime, fitness, color='green')

            fitness = [gen.averageFitness for gen in run]
            ax[x][y].plot(xTime, fitness, color='yellow')

    averageBestFitness /= len(generationData)

    plt.show()

    return averageBestFitness

geneticAverages = Algorithm_Evaluation(GeneticAlgorithm)
antColonyAverages = Algorithm_Evaluation(AntColonyAlgorithm)
psoAverages = Algorithm_Evaluation(pso)

# Average Algorithm Times
plt.figure(1)
plt.title("Average Algorithm Times")
plt.bar(["Genetic Algorithm", "Ant Colony Algorithm", "Particle Swarm Optimisation"],
        [geneticAverages[0], antColonyAverages[0], psoAverages[0]])

# Average Memory Usage
plt.figure(2)
plt.title("Average Memory Usage")
plt.bar(["Genetic Algorithm", "Ant Colony Algorithm", "Particle Swarm Optimisation"],
        [geneticAverages[1], antColonyAverages[1], psoAverages[1]])

# Average Best Fitness
plt.figure(3)
plt.title("Average Best Fitness")
plt.bar(["Genetic Algorithm", "Ant Colony Algorithm", "Particle Swarm Optimisation"],
        [geneticAverages[2], antColonyAverages[2], psoAverages[2]])

plt.show()

