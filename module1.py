from soupsieve import select
from module2 import *
from module2 import select_survivors


def init(pop_size, gen_num, cross_prob, mut_prob):
    x_gen = generate_init_pop(pop_size)  # generation 0
    f_gen = evaluate(x_gen)

    for gen in gen_num:
        x_par = select_parents(x_gen)
        x_new_par = crossover(x_par)
        x_child = mutation(x_new_par)
        x_next_gen = select_survivors(x_child)
        f_net_gen = evaluate(x_new_gen)
    

def generate_init_pop(pop_size):
    pass # return array of 195 bits

def evaluate(x_gen):
    pass # return array of fitness values