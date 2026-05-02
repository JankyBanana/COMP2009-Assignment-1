import numpy as np
import random
from common_functions import GenerationData

from common_functions import *

# Take a random sample of the population, and select the highest fitness gene from that sample
def SelectRandomHighFitnessSolution(population):
    sampleSize = 5
    solution = random.sample(population, sampleSize)
    solution = max(solution, key=lambda x: x[1])
    return solution

# Crossover function that randomly splits parents into offspring
def Crossover(parent1, parent2):
    # Random cut off point where the parent gene gets split
    cutpoint = random.randint(1, len(parent1) - 2)

    # Offspring
    child1 = np.concatenate([parent1[:cutpoint], parent2[cutpoint:]])
    child2 = np.concatenate([parent2[:cutpoint], parent1[cutpoint:]])

    return child1, child2

# Genetic Algorithm with optional arguments of generations, population size per generation, crossover probability, and mutation probability
def GeneticAlgorithm(generations = 500, populationSize = 50, crossoverProbability = 0.8, mutationProbability = 0.2):

    population = []
    generationData = []

    # Set the population to a list of random solutions
    for i in range(populationSize):
        # Generate random solution
        solution = GenerateRandomSolution()
        # Fitness is negative of the cost (higher cost = lower fitness_
        fitness = -TotalCostOfSolution(solution)
        population.append([solution, fitness])

    bestSolution = population[0]
    # Solution found is true if a solution with a fitness / cost of exactly 0 is found
    solutionFound = False

    # Main loop for each generation
    for generation in range(generations):
        # population.sort(key=lambda x: x[1], reverse=True)
        offspring = []
        costs = []

        # Loop to make a new population of offspring
        while len(offspring) < populationSize:
            # Choose a pair of high fitness parents
            parent1 = SelectRandomHighFitnessSolution(population)[0]
            parent2 = SelectRandomHighFitnessSolution(population)[0]

            # Crossover probability check
            if random.random() < crossoverProbability:
                child1, child2 = Crossover(parent1, parent2)
                offspring.append(child1)

                # Check to ensure adding another offspring won't exceed population size
                if len(offspring) < populationSize:
                    offspring.append(child2)

        # Mutation, go over each chromosome in the new offspring population and have a probability to mutate
        for individual in offspring:
            for index in range(len(individual)):
                if random.random() < mutationProbability:
                    # Mutate chromosome to random employee assigned to that task
                    individual[index] = random.randint(0, len(employees) - 1)

        # Set population to the new generation of offspring with calculated fitness
        population = []
        for i in range(populationSize):
            fitness = -TotalCostOfSolution(offspring[i])
            costs.append(fitness)

            # Check if current solution is better than the best found solution
            if fitness > bestSolution[1]:
                bestSolution = [offspring[i], fitness, generation]

                # Check if this is the best possible solution (no penalties)
                if fitness >= 0:
                    solutionFound = True

            population.append([offspring[i], fitness])

        # print("-------------NEW GENERATION-----------------")
        # for solution in population:
        #     print(solution[0], solution[1])

        generationData.append(GenerationData(min(costs), sum(costs) / len(costs), max(costs), bestSolution[1]))

        if solutionFound:
            break

    return generationData

    # print("------------------FINISHED-----------------")
    # for solution in population:
    #     print(solution[0], solution[1])

    print('---------------BEST SOLUTION--------------')
    print(bestSolution[0], bestSolution[1], bestSolution[2])


GeneticAlgorithm()
