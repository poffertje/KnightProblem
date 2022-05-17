from soupsieve import select
from module2 import *


def init(pop_size, gen_num, cross_prob, mut_prob):
    x_gen = generate_init_pop(pop_size)  # generation 0
    # Evaluate the initial generation
    f_gen = evaluate(x_gen)

    # Do the following for n generations
    for gen in range(gen_num):
        # Create a new population (i.e., loop until the population size is full)
        x_next_gen = np.empty((0,))
        while len(x_next_gen) < pop_size:
            x_par = select_parents(x_gen, f_gen)
            x_new_par = crossover(x_par, cross_prob)
            # There are multiple new individuals, but mutation only takes one
            x_child = mutation(x_new_par, mut_prob)
            x_next_gen = select_children(x_gen, x_child)
            f_next_gen = evaluate(x_next_gen)
            # We need to yield the best fitness here
        x_gen = x_next_gen
        f_gen = f_next_gen

    
# Takes population size as input and return an initial population
def generate_init_pop(pop_size):
    # Initialize an array for the population
    population = np.empty((0, 195), dtype=int)
    for i in range(pop_size):
        # Choose the starting position (between 0 and 63, 6 bits)
        individual = np.random.randint(2, size=6)
        # Generate 63 random transitions
        while len(individual) < 195:
            # All transition possibilities are 0-7, 3 bits
            transition = np.random.randint(2, size=3)
            individual = np.concatenate((individual, transition))
        # Add the new individual to the population
        population = np.concatenate((population, [individual]))
    # return array of arrays of 195 bits
    return population

# This is not the most effective way, but works for now
# Takes a generation as input and returns the fitnesses of the individuals
# of that population
def evaluate(x_gen):
    # Initialize an empty array for the fitnesses
    x_fitness = np.empty((0,))
    for individual in x_gen:
        # Calculate the fitness of that individual
        fitness_individual = 0
        # Keep a list of visited squares (The start square is visited, 
        # integers not binary numbers)
        visited = np.array([int(''.join(individual[:6].astype(str)), 2)])
        # For every transition, check whether it is on board & not visited
        for i in range(6, 195, 3):
            # Get the next square & whether it is a legal move
            next_square, legal = legal_move(visited, individual[i:(i+3)])
            # If yes, increment the fitness value
            if legal:
                fitness_individual += 1
            # Add the current square to the visited
            visited = np.concatenate((visited, [next_square]))
        # Add the fitness of the individual to the array
        x_fitness = np.concatenate((x_fitness, [fitness_individual]))

    return x_fitness # return array of fitness values

# This function takes as an input the visited squares and the current 
# transition and returns whether the transition is legal (i.e., on board & 
# not visited before)
def legal_move(visited, transition):
    # Translate the transition into number 0 to 7 (they are encoded, so that
    # 0 is up and left, and the rest are in clockwise order)
    if np.all(transition == [0, 0, 0]):
        new_square = visited[-1] - 2*8 - 1
    elif np.all(transition == [0, 0, 1]):
        new_square = visited[-1] - 2*8 + 1
    elif np.all(transition == [0, 1, 0]):
        new_square = visited[-1] - 8 + 2
    elif np.all(transition == [0, 1, 1]):
        new_square = visited[-1] + 8 + 2
    elif np.all(transition == [1, 0, 0]):
        new_square = visited[-1] + 2*8 + 1
    elif np.all(transition == [1, 0, 1]):
        new_square = visited[-1] + 2*8 - 1
    elif np.all(transition == [1, 1, 0]):
        new_square = visited[-1] + 8 - 2
    elif np.all(transition == [1, 1, 1]):
        new_square = visited[-1] - 8 - 2
    
    if np.where(visited != new_square):
        # Check whether the new square is on board
        if new_square < 64 and -1 < new_square:
            return new_square, True
        else:
            return new_square, False
    return new_square, False

