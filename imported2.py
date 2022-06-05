import numpy as np

''' DOCUMENTATION
The implementation of the Knight's Tour Problem consists of two modules. 
Module 1 contains the central loop while Module 2 contains the genetic operators.
To run the code, run Module 1 (because Module 2 is called from Module 1). 
You can alter the arguments for the evolutionary algorithm in Module 1.
The output is the best fitness value for each 10th generation.
'''

def pselection(x_old, f_old, k, p):
    # tournament selection

    x_parents = np.asarray([x_old[0]])
    f_parents = np.asarray([f_old[0]])
    for r in range(k-1):
        pick_index = np.random.randint(1, len(x_old), p)
        best_index = pick_index[0]
        best_value = f_old[pick_index[0]]
        for i in pick_index[1:]:
            value = f_old[i]
            if value > best_value:
                best_index = i
                best_value = value

        x_parents = np.concatenate([x_parents, [x_old[best_index]]])

        f_parents = np.concatenate([f_parents, [f_old[best_index]]])

    return x_parents, f_parents


def mutation(tours, mutation_rate):
    # takes one individual plus the mutation rate and 
    # returns one (possibly mutated) individual
    global mc
    to_mutate = int(tours.shape[0] * mutation_rate)
    indexmutate = np.random.randint(0, tours.shape[0], to_mutate)
    for i in indexmutate:
        indind = np.random.randint(0, len(tours[0]), np.random.randint(len(tours[0])))
        for j in indind:
            mc = tours[i]
            np.delete(tours, i)
            mc = list(mc)
            if mc[j] == '0':
                mc[j] = '1'
            else:
                mc[j] = '0'
            mc = "".join(mc)
        tours = np.concatenate([tours, [mc]])
    return tours



def crossover(parents):
    # creates empty list for the children
    new_x_children = []

    while len(new_x_children) < (parents.size):
        # selects two parents from the x amount of parents before
        iparents = np.random.randint(parents.shape[0], size=2)
        parent1 = parents[iparents[0]]
        parent2 = parents[iparents[1]]
        # creates a random point in the bit sequence
        points = np.random.randint(1, len(parent1) - 1, int(len(parent1)/2))
        # from that point onwards the parents bit sequences are changed
        new_child = list(parent1)
        for i in points:
            new_child[i] = parent2[i]
        # this mixed parent is added to the list of children
        new_child = "".join(new_child)
        new_x_children.append(new_child)

    return np.array(new_x_children)



def survivor_selection(x_old, x_children, f_old, f_children):
    sr = int(len(x_old) * np.random.uniform(0.5, 1))
    x_o = x_old[:sr]
    f_o = f_old[:sr]
    x_cat = np.concatenate([x_children, x_o], 0)
    f_cat = np.concatenate([f_children, f_o])
    ind = np.argsort(f_cat)
    ind = np.flip(ind)
    x = x_cat[ind]
    f = f_cat[ind]
    xn = x[:int(x.size/2)]
    fn = f[:int(x.size/2)]
    rindices = np.random.randint(int(x.size/2), int(x.size), int(x.size/4))
    for i in rindices:

        xn = np.concatenate([xn, [x[i]]])
        fn = np.concatenate([fn, [f[i]]])

    return xn,fn