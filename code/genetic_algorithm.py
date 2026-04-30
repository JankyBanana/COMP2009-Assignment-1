import numpy as np
import random

from common_functions import *

def SelectRandomHighFitnessSolution(population):
    sampleSize = 5
    solution = random.sample(population, sampleSize)
    solution = max(solution, key=lambda x: x[1])
    #solution.sort(key=lambda x: x[1], reverse=True)
    return solution


def Crossover(parent1, parent2):
    cutpoint = random.randint(1, len(parent1) - 2)
    child1 = np.concatenate([parent1[:cutpoint], parent2[cutpoint:]])
    child2 = np.concatenate([parent2[:cutpoint], parent1[cutpoint:]])

    return child1, child2


def GeneticAlgorithm():
    crossoverProbability = 0.8
    mutationProbability = 0.2
    generations = 200
    populationSize = 50

    population = []
    for i in range(populationSize):
        solution = GenerateRandomSolution()
        fitness = -TotalCostOfSolution(solution)
        population.append([solution, fitness])
    bestSolution = population[0]

    for generation in range(generations):

        population.sort(key=lambda x: x[1], reverse=True)
        offspring = []

        while len(offspring) < populationSize:
            parent1 = SelectRandomHighFitnessSolution(population)[0]
            parent2 = SelectRandomHighFitnessSolution(population)[0]

            if random.random() < crossoverProbability:
                child1, child2 = Crossover(parent1, parent2)
                offspring.append(child1)
                if len(offspring) < populationSize:
                    offspring.append(child2)

        for individual in offspring:
            for index in range(len(individual)):
                if random.random() < mutationProbability:
                    individual[index] = random.randint(0, len(employees) - 1)

        population = []
        for i in range(populationSize):
            fitness = -TotalCostOfSolution(offspring[i])
            if fitness > bestSolution[1]:
                bestSolution = [offspring[i], fitness, generation]
            population.append([offspring[i], fitness])

        print("-------------NEW GENERATION-----------------")
        for solution in population:
            print(solution[0], solution[1])

    print("------------------FINISHED-----------------")
    for solution in population:
        print(solution[0], solution[1])

    print('---------------BEST SOLUTION--------------')
    print(bestSolution[0], bestSolution[1], bestSolution[2])


GeneticAlgorithm()
