import numpy as np

class Employee:
    def __init__(self, employeeID, availableHours, skillLevel, skills):
        self.employeeID = employeeID
        self.availableHours = availableHours
        self.skillLevel = skillLevel
        self.skills = skills

class Task:
    def __init__(self, taskID, estimatedTime, difficulty, deadline, requiredSkill):
        self.taskID = taskID
        self.estimatedTime = estimatedTime
        self.difficulty = difficulty
        self.deadline = deadline
        self.requiredSkill = requiredSkill

employees = [Employee('E1', 10, 4, ['A','C']),
             Employee('E2', 12, 6, ['A','B','C']),
             Employee('E3', 8, 3, ['A']),
             Employee('E4', 15, 7, ['B','C']),
             Employee('E5', 9, 5, ['A','C'])]

tasks = [Task('T1', 4, 3, 8, 'A'),
         Task('T2', 6, 5, 12, 'B'),
         Task('T3', 2, 2, 6, 'A'),
         Task('T4', 5, 4, 10, 'C'),
         Task('T5', 3, 1, 7, 'A'),
         Task('T6', 8, 6, 15, 'B'),
         Task('T7', 4, 3, 9, 'C'),
         Task('T8', 7, 5, 14, 'B'),
         Task('T9', 2, 2, 5, 'A'),
         Task('T10', 6, 4, 11, 'C')]

def GenerateRandomSolution():
    return np.random.randint(0, len(employees), len(tasks))

def GetEmployeeTasks(employeeIndex, solution):
    employeeTasks = []
    index = 0
    for i in solution:
        if i == employeeIndex:
            employeeTasks.append(tasks[index])
        index += 1
    return employeeTasks


def CalculateDeadlineViolationPenalty(solution):
    deadlineViolationPenalty = 0

    for employeeIndex in range(0, len(employees)):
        employeeTasks = GetEmployeeTasks(employeeIndex, solution)

        if employeeTasks is not None:
            employeeTasks = sorted(employeeTasks, key=lambda task: task.estimatedTime)

            # print(employeeTasks)
            # for task in employeeTasks:
            #     print(task.estimatedTime)

            FinishTime = 0

            for task in employeeTasks:
                FinishTime += task.estimatedTime
                deadlineViolationPenalty += max(FinishTime - task.deadline, 0)
    return deadlineViolationPenalty

def CalculateOverloadPenalty(solution):
    overloadPenalty = 0
    for employeeIndex in range(0, len(employees)):
        totalHours = 0
        employeeTasks = GetEmployeeTasks(employeeIndex, solution)

        if employeeTasks is not None:
            for task in employeeTasks:
                totalHours += task.estimatedTime
            overloadPenalty += max(0, totalHours - employees[employeeIndex].availableHours)

    return overloadPenalty

def CalculateSkillMismatchPenalty(solution):
    skillMismatchPenalty = 0

    taskIndex = 0
    for task in solution:

        if tasks[taskIndex].requiredSkill not in employees[task].skills:
            skillMismatchPenalty += 1

        taskIndex += 1

    return skillMismatchPenalty

def CalculateDifficultyViolationPenalty(solution):
    difficultyViolationPenalty = 0

    taskIndex = 0
    for employeeIndex in solution:
        if employees[employeeIndex].skillLevel < tasks[taskIndex].difficulty:
            difficultyViolationPenalty += 1
        taskIndex += 1

    return difficultyViolationPenalty

def TotalCostOfSolution(solution):
    # uniqueAssignmentPenalty = CalculateUniqueAssignmentPenalty(solution)
    uniqueAssignmentPenalty = 0
    deadlineViolationPenalty = CalculateDeadlineViolationPenalty(solution)
    overloadPenalty = CalculateOverloadPenalty(solution)
    skillMismatchPenalty = CalculateSkillMismatchPenalty(solution)
    difficultyViolationPenalty = CalculateDifficultyViolationPenalty(solution)

    totalCost = 0.2 * (uniqueAssignmentPenalty + deadlineViolationPenalty + overloadPenalty + skillMismatchPenalty + difficultyViolationPenalty)
    return totalCost