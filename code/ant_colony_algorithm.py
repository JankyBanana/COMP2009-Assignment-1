import math

import numpy as np
import random

from common_functions import *

def solutionConstruction(pheromone):
    solution = []
    for row in pheromone:
        totalPheromone = sum(row)
        if totalPheromone == 0:
            employee = random.randint(0, len(employees) - 1)
            solution.append(employee)
            continue

        r = random.uniform(0, totalPheromone)
        cumulative = 0
        chosenEmployee = 0

        for employee in range(len(employees)):
            cumulative += row[employee]
            if cumulative >= r:
                chosenEmployee = employee
                break

        solution.append(chosenEmployee)


    return solution


def AntColonyAlgorithm():
    pheromone = np.ones((len(tasks), len(employees)))
    numberOfAnts = 50
    evaporationRate = 0.5
    depositConstant = 2
    generations = 200

    solutions = []
    fitnesses = []
    bestSolution = (None, -math.inf)

    for generation in range(generations):
        # Ants choose solution
        for ant in range(numberOfAnts):
            solution = solutionConstruction(pheromone)
            fitness = -TotalCostOfSolution(solution)
            fitnesses.append(fitness)
            solutions.append(solution)
            if fitness > bestSolution[1]:
                bestSolution = (solution, fitness)
                if fitness >= 0:
                    print(bestSolution, generation)

        # Evaporate
        for row in pheromone:
            for column in row:
                column *= (1 - evaporationRate)

        # Deposit
        i = 0
        for solution in solutions:
            deposit_amount = depositConstant / ((0 - fitnesses[i]) + 1)

            ii = 0
            for employee in solution:
                pheromone[ii][employee] += deposit_amount
                ii += 1
            i += 1

    print("Best solution is:", bestSolution[0], bestSolution[1])
    return bestSolution


#GeneticAlgorithm()
AntColonyAlgorithm()