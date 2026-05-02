#
# Implementation of a particle swarm optimisation algorithm for Assignment 1
#
# The solution vector of each particle encodes a candidate solution using an
# array where (index, value) = (task, assigned employee).
#
# Particle fitness evaluated using constraint violations.
#
# Algorithm modifications to improve algorithm efficiency include:
# - Candidate solutions (position vectors) as combinations of unique row and column positions
# - Regenerating part of the swarm when stagnation is detected
#

import random as r
import common_functions as cf

GREEN = "\033[32m"
RESET = "\033[0m"

DEBUG = 0


class PSOConfig:
    def __init__(self, size=20, pw=0.5, gw=0.5, w=0.5, v_max=4.0, stag_lim=10, max_iter=500):
        self.size = size
        self.pw = pw  # Personal best weight
        self.gw = gw  # Group best weight
        self.w = w  # Previous velocity inertia
        self.v_max = v_max  # Max absolute value of velocity vector i.e. -v_max < v < v_max
        self.stag_lim = stag_lim  # Number of iterations with no improvement to trigger swarm regeneration
        self.regen_size = self.size // 2  # Number of particles to regenerate
        self.max_iterations = max_iter


class Particle:
    def __init__(self):
        self.solution = []
        self.vel = []
        self.p_best = None
        self.p_best_cost = float('-inf')


def pso(cfg=None):
    # If no cfg provided use default algorithm parameters
    if cfg is None:
        cfg = PSOConfig()

    # Initialising PSO simulation parameters
    pw = cfg.pw
    gw = cfg.gw
    w = cfg.w
    v_max = cfg.v_max
    stag_lim = cfg.stag_lim
    iteration = 0
    regens = 0
    stagnation = 0
    max_iteration = cfg.max_iterations

    gen_data_list = []

    # Swarm initialisation
    swarm_list = create_swarm(cfg.size)

    if DEBUG == 1:
        print_swarm(swarm_list)

    cost_list = swarm_cost(swarm_list)
    g_best_idx = cost_list.index(max(cost_list))
    g_best_pos = swarm_list[g_best_idx].solution

    if DEBUG:
        print(f"|DEBUG| g_best_pos: {g_best_pos}")
        print(f"|DEBUG| g_best_idx = {g_best_idx}\n")

    # Start of main PSO loop
    while max(cost_list) < 0 and iteration < max_iteration:
        # Regenerate part of swarm if stagnation detected
        if stagnation >= stag_lim:
            if DEBUG:
                print(f"|DEBUG| stagnation = {stagnation}. Regenerating swarm.\n")
            regen_swarm(swarm_list, cost_list, cfg)
            regens += 1
            stagnation = 0

        iteration += 1

        # Updating each particle's velocity and position vectors
        for p_idx, p in enumerate(swarm_list):
            if DEBUG:
                print(f"|DEBUG| ----- Particle {p_idx} -----")
                print(f"|DEBUG| |Before| p.solution: {p.solution}")
                print(f"|DEBUG| |Before| p.vel: {p.vel}")

            for vect_idx in range(len(p.solution)):
                # Updating velocity vector components
                r1 = r.random()
                r2 = r.random()
                new_vel = round(w * p.vel[vect_idx] +
                                pw * r1 * (p.p_best[vect_idx] - p.solution[vect_idx]) +
                                gw * r2 * (g_best_pos[vect_idx] - p.solution[vect_idx]), 3)
                # Check effect, required or not?
                p.vel[vect_idx] = max(-v_max, min(v_max, new_vel))  # Clamping velocity components

                # Updating position vector components
                if DEBUG:
                    print(
                        f"|DEBUG| new_pos[{vect_idx}] = {p.solution[vect_idx]} + {p.vel[vect_idx]} = {p.solution[vect_idx] + p.vel[vect_idx]}")
                new_pos = round((p.solution[vect_idx] + p.vel[vect_idx])) % len(cf.employees)
                p.solution[vect_idx] = new_pos

            if DEBUG:
                print(f"|DEBUG| |After| p.solution: {p.solution}")
                print(f"|DEBUG| |After| p.vel: {p.vel}\n")

        # Calculate new swarm fitness and track stagnation
        new_cost_list = swarm_cost(swarm_list)
        if max(new_cost_list) <= max(cost_list):
            stagnation += 1
        else:
            stagnation = 0

        if DEBUG:
            if DEBUG: print(f"|DEBUG| Old cost_list: {cost_list}  max = {max(cost_list)}")
            if DEBUG: print(
                f"|DEBUG| New cost_list: {new_cost_list}  max = {max(new_cost_list)}")
            if DEBUG: print(f"|DEBUG| stagnation = {stagnation}")

        # Update 'p_best' if new p.solution better than p.p_best
        for p_idx, p in enumerate(swarm_list):
            if new_cost_list[p_idx] > p.p_best_cost:
                p.p_best = p.solution.copy()
                p.p_best_cost = new_cost_list[p_idx]

        # Update fitness list and g_best_idx/pos
        cost_list = new_cost_list
        g_best_idx = cost_list.index(max(cost_list))
        g_best_pos = swarm_list[g_best_idx].solution.copy()

        if DEBUG:
            print(f"|DEBUG| Iteration {iteration}:")
            print(f"|DEBUG|  - g_best_pos: {g_best_pos}")
            print(f"|DEBUG|  - g_best_vel: {swarm_list[g_best_idx].vel}")
            print(f"|DEBUG|  - cost_list: {cost_list}")
            input("")

        average_cost = sum(cost_list) / len(cost_list)
        gen_data = cf.GenerationData(min(cost_list), average_cost, max(cost_list),
                                     -cf.TotalCostOfSolution(g_best_pos))
        gen_data_list.append(gen_data)

    print(
        f"Found solution: {g_best_pos} cost = {cf.TotalCostOfSolution(g_best_pos)}, after {iteration} iterations ({regens} regenerations)")

    return gen_data_list


def create_swarm(swarm_size: int) -> list[Particle]:
    swarm_list = []
    for i in range(swarm_size):
        swarm_list.append(create_particle())

    return swarm_list


def create_particle() -> Particle:
    particle = Particle()
    particle.solution = cf.GenerateRandomSolution()
    particle.vel = cf.GenerateRandomSolution()
    particle.p_best = particle.solution[:]

    return particle


def swarm_cost(swarm_list: list[Particle]):
    cost_list = []

    for idx, particle in enumerate(swarm_list):
        if DEBUG:
            print(f"|DEBUG| ----- Particle {idx} -----")

        p_cost = round(-cf.TotalCostOfSolution(particle.solution), 3)
        cost_list.append(p_cost)

        if DEBUG:
            print(f"|DEBUG| solution: {particle.solution}")
            print(f"|DEBUG| cost = {p_cost}")
            print(f"|DEBUG| cost_list = {cost_list}\n")

    return cost_list


def regen_swarm(swarm_list: list[Particle], fitness_list: list[int], cfg: PSOConfig):
    """
    Regenerate the lowest fitness particles in 'swarm_list' as new particles.

    Number of particles to regenerate defined by 'cfg.regen_num'. Defaults to
    half of 'cfg.size'.
    """
    if DEBUG:
        print(f"|DEBUG| old swarm_list:")
        print_swarm(swarm_list)
        print(f"|DEBUG| old fitness_list: {fitness_list}")

    for i in range(cfg.regen_size):
        min_idx = fitness_list.index(min(fitness_list))
        if DEBUG:
            print(f"min_idx = {min_idx}\n")
        swarm_list[min_idx] = create_particle()

    fitness_list[:] = swarm_cost(swarm_list)

    if DEBUG:
        print(f"|DEBUG| new swarm_list:")
        print_swarm(swarm_list)
        print(f"|DEBUG| new fitness_list: {fitness_list}")


def print_swarm(swarm_list: list):
    print("|DEBUG| Swarm list:")
    for p in swarm_list:
        print(f"|DEBUG| {p.solution} {p.vel} {p.p_best}")

    print("")


if __name__ == "__main__":
    DEBUG = 0
    pso_cfg = PSOConfig(size=20, pw=0.5, gw=0.5, w=0.5, max_iter=500)
    # solution, cost, iterations, regenerations = pso(pso_cfg)
