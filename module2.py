from random import randint
import numpy as np

GENE_SIZE = 195
NUM_PARENTS = 80 # creates twice the number of children


class EA(object):
    def __init__(self, pop_size, cross_prob, mut_prob):
        self.pop_size = pop_size
        self.crossover_p = cross_prob
        self.mutation_p = mut_prob

    # probabilistically picks two individuals from a population,
    # weighted by their fitness: Roulette Selection
    def parent_selection(self, x_old, f_old):
        # type: (list[str], list(int)) -> list[str]

        x_parents = []  # intialize return array
        f_sum = sum(f_old)  # sum of f_values

        for i in range(NUM_PARENTS):
            # create a random point P between 0 and f_sum
            point_P = randint(0, f_sum)
            # keep adding fitness values to point_P until point_P exceeds f_sum
            for count, (f_gene, x_gene) in enumerate(zip(f_old, x_old)):
                point_P += f_gene
                # make an individual that exceeds f_sum new parent
                if point_P >= f_sum:
                    x_parents.append(x_gene)
                    break  # start the next spin

                # if we have not exceeded the sum, then pick the last element
                elif point_P < f_sum and count == (self.pop_size - 1):
                    x_parents.append(x_gene)
                    break  # start the next spin

        return x_parents

    # Apply random one-point crossover to get new individuals
    def recombination(self, x_parents):
        # type: (list[str]) -> list[str]

        x_children = []  # initialize return variable

        for idx in range(len(x_parents)):
            # select 2 genomes to become parents for crossover
            parent1, parent2 = x_parents[idx], x_parents[- 1 - idx]
            # typecast the parents into lists
            par1, par2 = list(parent1), list(parent2)

            # pick a random value from uniform distribution between 0 and 1
            random_p = np.random.uniform(0, 1)

            # if the random value is less than the crossover probability,
            # recombinate the parents
            if random_p < self.crossover_p:
                # pick a random crossover point
                recombination_point = randint(0, GENE_SIZE)

                for i in range(recombination_point, GENE_SIZE):
                    # create children
                    par1[i], par2[i] = par2[i], par1[i]

                child1 = ''.join(par1)
                child2 = ''.join(par2)

            # else the original parents are new children
            else:
                child1 = parent1
                child2 = parent2

            # put the children into the return array
            x_children.extend([child1, child2])

        return x_children

    # The mutation method takes the mutation probability and an individual as
    # input and returns possibly mutated individual: Bit flipping
    def mutation(self, x_children):
        # type: (list[str]) -> list[str]

        x_new_children = []  # initialize the return value

        for child in x_children:

            # pick a random value from uniform distribution between 0 and 1
            random_p = np.random.uniform(0, 1)
            # typecast to list
            ret_child = list(child)

            # If the value is less than the mutation probability,
            # mutate the individual
            if random_p < self.mutation_p:
                # choose a random bit to flip
                mutation_point = randint(0, GENE_SIZE - 1)

                if ret_child[mutation_point] == '0':
                    ret_child[mutation_point] = '1'

                else:
                    ret_child[mutation_point] = '0'

            # add the children to the new return array
            x_new_children.append(''.join(ret_child))

        return x_new_children

    # the children selection method takes a population and an individual
    # as input and returns their union
    def survivor_selection(self, x_old, f_old, x_new_children):
        # sort the population based on fitness value
        sorted_pop = (sorted(zip(x_old, f_old), key=lambda x: x[1]))
        # get generation chromosomes from sorted list
        x_sort = [x for x, _ in sorted_pop]
        # drop the genes with smallest fitness to make room for children
        x_survivours = [*x_sort[NUM_PARENTS*2:], *x_new_children]

        return x_survivours

    def step(self, x_old, f_old):
        # type: (list[str], list(int)) -> list[str]

        # select the parents
        x_parents = self.parent_selection(x_old, f_old)
        # recombine the parents to create children
        x_children = self.recombination(x_parents)
        # mutate the resulting the resulting children
        x_new_children = self.mutation(x_children)
        # select the survivors and return them
        x_survivours = self.survivor_selection(x_old, f_old, x_new_children)

        return x_survivours
