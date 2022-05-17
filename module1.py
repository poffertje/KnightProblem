from soupsieve import select
from module2 import *


def init(pop_size, gen_num, cross_prob, mut_prob):
    x_gen = generate_init_pop(pop_size)  # generation 0
    # Evaluate the initial generation
    f_gen = evaluate(x_gen)

    for gen in gen_num:
        x_par = select_parents(x_gen)
        x_new_par = crossover(x_par, cross_prob)
        x_child = mutation(x_new_par, mut_prob)
        x_next_gen = select_children(x_gen, x_child)
        f_next_gen = evaluate(x_next_gen)
    
# Takes population size as input and return an initial population
def generate_init_pop(pop_size):
    # Initialize an array for the population
    population = np.empty((0, 195))
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

# Takes a generation as input and returns the fitnesses of the individuals
# of that population
def evaluate(x_gen):
    pass
