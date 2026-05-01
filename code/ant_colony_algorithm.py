import math

import numpy as np
import random

from common_functions import *

def solutionConstruction(pheromone):
    solution = []
    for row in pheromone:
        totalPheromone = sum(row)
        if totalPheromone <= 0:
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


def AntColonyAlgorithm(generations = 500, numberOfAnts = 30, evaporationRate = 0.2, depositConstant = 0.4):
    pheromone = np.ones((len(tasks), len(employees)))
    maxPheromone = 10

    bestSolution = (None, -math.inf)
    solutionFound = False

    for generation in range(generations):
        solutions = []
        fitnesses = []
        # Ants choose solution
        for ant in range(numberOfAnts):
            solution = solutionConstruction(pheromone)
            fitness = -TotalCostOfSolution(solution)
            fitnesses.append(fitness)
            solutions.append(solution)
            if fitness > bestSolution[1]:
                bestSolution = (solution, fitness)
                print(bestSolution, generation)
                if fitness >= 0:
                    print(bestSolution, generation)
                    solutionFound = True

        # Evaporate
        for row in range(len(pheromone)):
            for column in range(len(pheromone[row])):
                pheromone[row][column] *= (1 - evaporationRate)

        # Deposit
        i = 0
        for solution in solutions:
            deposit_amount = depositConstant / ((-10*fitnesses[i]) + 1)

            ii = 0
            for employee in solution:
                pheromone[ii][employee] += deposit_amount
                if pheromone[ii][employee] > maxPheromone:
                    pheromone[ii][employee] = maxPheromone
                ii += 1
            i += 1

        if solutionFound:
            break

    print("Best solution is:", bestSolution[0], bestSolution[1])
    return bestSolution


#GeneticAlgorithm()
AntColonyAlgorithm()