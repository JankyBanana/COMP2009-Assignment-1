import matplotlib.pyplot as plt
import tracemalloc
import numpy as np

from genetic_algorithm import GeneticAlgorithm
from ant_colony_algorithm import AntColonyAlgorithm

import time


def Algorithm_Evaluation(algorithm_function):
    algorithmTimes = []
    memoryData = []
    timeX = np.arange(0, 20, 1)
    generationData = []


    for i in range(20):
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

    Plot_Algorithm_Generation_Data(generationData)

def Plot_Algorithm_Generation_Data(generationData):
    fig, ax = plt.subplots(4, 5)
    for x in range(4):
        for y in range(5):
            index = x * 5 + y
            run = generationData[index]

            fitness = [gen.bestFitness for gen in run]
            xTime = np.arange(0, len(fitness), 1)
            ax[x][y].plot(xTime, fitness, color='blue')

            fitness = [gen.minFitness for gen in run]
            ax[x][y].plot(xTime, fitness, color='red')

            fitness = [gen.maxFitness for gen in run]
            ax[x][y].plot(xTime, fitness, color='green')

            fitness = [gen.averageFitness for gen in run]
            ax[x][y].plot(xTime, fitness, color='yellow')

    plt.show()

Algorithm_Evaluation(GeneticAlgorithm)
Algorithm_Evaluation(AntColonyAlgorithm)

# plt.plot(timeX, geneticTimes)
