from random import randint

GENE_SIZE = 195

class EA(object):
    def __init__(self, pop_size, cross_prob, mut_prob):
        self.pop_size = pop_size
        self.crossover_p = cross_prob
        self.mutation_p = mut_prob

    def parent_selection(self, x_old, f_old):
        pass

    # Apply random one-point crossover to get new individuals
    def recombination(self, x_parents, f_parents):
        # type: (list[str], list[int]) -> list[str]

        # pick a random crossover point
        recombination_point = randint(0, GENE_SIZE)
        
        flag=0
        for i in range(GENE_SIZE):
            if flag==0:
                child.gene_pool[i] = self.gene_pool[i]
                if i==crossover_point:
                    flag = 1
            elif flag==1:
                child.gene_pool[i] = mate.gene_pool[i]
        return child


    def mutation(self, old_x_children, old_f_children):
        pass


    def survivor_selection(self, x_children, x_old, f_children, f_old):
        pass

    def step(self, x_old, f_old):
        pass