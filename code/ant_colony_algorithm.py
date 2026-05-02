import math

import numpy as np
import random

from common_functions import *

# How each ant constructs a solution given the pheromone matrix
def solutionConstruction(pheromone):
    solution = []

    # For each pheromone for task i
    for row in pheromone:
        totalPheromone = sum(row)

        # If total pheromone is 0, select random employee for task
        if totalPheromone <= 0:
            employee = random.randint(0, len(employees) - 1)
            solution.append(employee)
            continue

        # Roulette wheel for weighted selection of employee given pheromone matrix
        # Random number between 0 and totalPheromone
        r = random.uniform(0, totalPheromone)
        cumulative = 0
        chosenEmployee = 0

        # Randomly select an employee with weighted probabilities given pheromone
        for employee in range(len(employees)):
            cumulative += row[employee]
            if cumulative >= r:
                chosenEmployee = employee
                break

        solution.append(chosenEmployee)


    return solution

# Ant Colony Algorithm with optional arguments for iterations (generations), number of ants per iteration, evaporation rate, and depositConstant
def AntColonyAlgorithm(generations = 500, numberOfAnts = 30, evaporationRate = 0.2, depositConstant = 0.4):
    pheromone = np.ones((len(tasks), len(employees)))
    # Max possible pheromone level to prevent severe stagnation from a single solution
    maxPheromone = 10

    # Best solution found so far
    bestSolution = (None, -math.inf)
    # SolutionFound = True if the best possible solution has been found (fitness / cost = 0)
    solutionFound = False

    # Main loop, iterates through each generation
    for generation in range(generations):
        solutions = []
        fitnesses = []

        # Ants choose solution
        for ant in range(numberOfAnts):
            # Generate solution
            solution = solutionConstruction(pheromone)
            # Determine fitness, which is the negative of cost (higher fitness = lower cost)
            fitness = -TotalCostOfSolution(solution)
            fitnesses.append(fitness)
            solutions.append(solution)

            # Check if this solution is the best so far
            if fitness > bestSolution[1]:
                bestSolution = (solution, fitness)
                print(bestSolution, generation)

                # Check if this solution is the best possible solution of fitness / cost = 0
                if fitness >= 0:
                    print(bestSolution, generation)
                    solutionFound = True

        # Evaporate pheromone to prevent stagnation and encourage exploration
        for row in range(len(pheromone)):
            for column in range(len(pheromone[row])):
                pheromone[row][column] *= (1 - evaporationRate)

        # Deposit pheromone based on solution fitness, higher fitness deposits more pheromone on their pheromone matrix
        i = 0
        # Iterate through each ant's solution to deposit pheromone
        for solution in solutions:
            # Calculate amount to be deposited
            deposit_amount = depositConstant / ((-10*fitnesses[i]) + 1)

            # Iterate through each task-employee assignment and deposit pheromone on ant's solution
            ii = 0
            for employee in solution:
                pheromone[ii][employee] += deposit_amount

                # Cap maximum phermone limit at maxPheromone
                if pheromone[ii][employee] > maxPheromone:
                    pheromone[ii][employee] = maxPheromone
                ii += 1
            i += 1

        # If best solution possible is found, terminate algorithm
        if solutionFound:
            break

    print("Best solution is:", bestSolution[0], bestSolution[1])
    return bestSolution


#GeneticAlgorithm()
AntColonyAlgorithm()