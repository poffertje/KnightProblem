import numpy as np

def select_parents():
    pass

def crossover():
    pass

# The mutation method takes the mutation probability and an individual as 
# input and returns possibly mutated individual
def mutation(individual, mutation_probability):
    # Pick a random value from uniform distribution between 0 and 1
    value = np.random.uniform(0, 1)
    # If the value is less than the mutation probability, mutate the individual
    if value < mutation_probability:
        # Choose random bit and flip it
        i = np.random.choice(len(individual))
        if individual[i]==0:
            individual[i] = 1
        else: 
            individual[i] = 0
    # Else, we will not mutate the individual
    return individual

# The select_children-method takes a population and an individual as input
# and returns their union
def select_children(population, individual):
    # Add the individual to the population
    new_pop = np.concatenate((population, [individual]))
    return new_pop
