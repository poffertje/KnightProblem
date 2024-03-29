from random import randint
from itertools import product
from module2 import EA

GENE_SIZE = 195
GENE_PIECE_POS = 6  # length of the initial position in bits
NUM_BITS = 3  # number of bits to encode moves


num_gen = 500
pop_size = 175
cross_prob = 0.9
mut_prob = 0.3
# use True if you want to see the best move sequence in the output
verbose = True


# This is the main loop of the evolutionary algorithm
def main(pop_size, num_gen, cross_prob, mut_prob):
    # initialize the population
    x_gen = generatePopulation(pop_size)  # create generation 0
    f_gen, _ = evaluate(x_gen)  # get the fitness value of generation 0

    # create an object for the evolutionary algorithm
    ea = EA(pop_size, cross_prob, mut_prob)

    for i in range(num_gen):
        # take a step with the genetic algorithm
        x_gen = ea.step(x_gen, f_gen)
        # evaluate the new generation
        f_gen, solutions = evaluate(x_gen)
        # get the index of the best value
        best_idx = f_gen.index(max(f_gen))
        # yield the concatenated results string
        yield (i, max(f_gen), solutions[best_idx])


# This function creates the initial population
# takes population size as input and return an initial population
def generatePopulation(pop_size):
    # type: (int) -> list[str]

    generation = []  # initialize return variable
    for i in range(pop_size):
        # create a single gene
        gene = ''
        for i in range(GENE_SIZE):
            # update single gene
            gene = gene + str(randint(0, 1))

        # check for errors before adding the gene to the gene pool
        try:
            assert len(gene) == GENE_SIZE
        except:
            raise Exception('Gene length must be {}, \
                            got {} instead'.format(GENE_SIZE, len(gene)))

        generation.append(gene)

    return generation


# Takes a generation as input and returns a list of the fitnesses of the
# individuals of that population
def evaluate(x_gen):
    # type: (list[str]) -> list[int] and list[int]

    f_gen = []  # list of fitness values
    solutions = []  # list of solutions

    for gene in x_gen:
        board = Board()
        f_gen.append(board.evaluateGene(gene))
        solutions.append(board.visited_cells)

    return f_gen, solutions


class Board:
    def __init__(self):
        self.x_axis = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.y_axis = [1, 2, 3, 4, 5, 6, 7, 8]

        self.cells = [(x, y) for x in self.x_axis
                      for y in self.y_axis]  # get all cells of the chess board

        self.positions = [x for x in range(0, 64)]  # iteration list

        self.cells_and_pos = zip(self.positions,
                                 sorted(self.cells, key=lambda x: x[1]))

        self.current_pos = None  # saves the current position of the piece
        self.visited_cells = []  # saves visited cells

    # Return all legal moves for the knight figure based on current position
    def getKnightMoves(self, position):
        # type: (tuple(str, int)) -> list[tuple(str, int)]
        x, y = position

        # create all posible moves for knight travel trajectory
        moves = list(product([chr(ord(x) - 1), chr(ord(x) + 1)],
                             [y - 2, y + 2])) + \
                list(product([chr(ord(x) - 2), chr(ord(x) + 2)],
                             [y - 1, y + 1]))

        # out of bounds check
        moves = [(x, y) for (x, y) in moves if (x, y) in self.cells]

        return moves

    # Binary code to cell on board converter
    def translateBinaryToCell(self, binary):
        # type: (str) -> tuple(str, int)

        # convert binary to decimal
        decimal = 0
        for digit in binary:
            decimal = decimal * 2 + int(digit)

        # match the resulting integer with location on chess board
        ret = [cell for pos, cell in self.cells_and_pos if decimal == pos]

        return ret[0]

    # Splits the gene into a list of moves
    def splitGene(self, gene):
        # type: (str) -> list[str]

        splitted_gene = []  # initialize return value
        # append the starting position
        splitted_gene.append(gene[0:GENE_PIECE_POS])

        # slice the gene without starting position
        gene_without_start = gene[GENE_PIECE_POS:len(gene)]

        # check for errors before splitting the gene
        try:
            assert len(gene_without_start) % NUM_BITS == 0
        except:
            raise Exception('Gene length must be a multiple of {}, \
                            got {} instead'.format(NUM_BITS, len(gene_without_start)))

        moves = [gene_without_start[i:i + NUM_BITS]
                 for i in range(0, len(gene_without_start), NUM_BITS)]

        splitted_gene.extend(moves)

        return splitted_gene

    # Make a move from the current position and returns new location
    def updatePosition(self, curr_pos, move):
        # type: (tuple(str, int), tuple(str, int)) -> tuple(str, int)

        if move == '000':
            location = (chr(ord(curr_pos[0]) + 1), curr_pos[1] - 2)

        elif move == '001':
            location = (chr(ord(curr_pos[0]) + 2), curr_pos[1] - 1)

        elif move == '010':
            location = (chr(ord(curr_pos[0]) + 2), curr_pos[1] + 1)

        elif move == '011':
            location = (chr(ord(curr_pos[0]) + 1), curr_pos[1] + 2)

        elif move == '100':
            location = (chr(ord(curr_pos[0]) - 1), curr_pos[1] + 2)

        elif move == '101':
            location = (chr(ord(curr_pos[0]) - 2), curr_pos[1] + 1)

        elif move == '110':
            location = (chr(ord(curr_pos[0]) - 2), curr_pos[1] - 1)

        elif move == '111':
            location = (chr(ord(curr_pos[0]) - 1), curr_pos[1] - 2)

        return location

    # Returns fitness value
    def evaluateGene(self, gene):
        # type: (str) -> int

        # check for errors before calculating fitness
        try:
            assert len(gene) == GENE_SIZE
        except:
            raise Exception('Gene length must be {}, \
                            got {} instead'.format(GENE_SIZE, len(gene)))

        fitness_value = 0

        # split the gene and get initial location of the piece
        splitted_gene = self.splitGene(gene)
        self.current_pos = self.translateBinaryToCell(splitted_gene[0])
        self.visited_cells.append(self.current_pos)

        # iterate through the moves and update fitness value
        for move in splitted_gene[1:len(splitted_gene)]:
            valid_moves = self.getKnightMoves(self.current_pos)
            location = self.updatePosition(self.current_pos, move)
            # check whether move is a valid one
            # and add one to the fitness value if yes
            if location in valid_moves and location not in self.visited_cells:
                fitness_value += 1
            # if the knight makes an illegal move, stop traversal
            else:
                return fitness_value

            # update the state of the board
            self.current_pos = location
            self.visited_cells.append(location)

        return fitness_value


result = main(pop_size, num_gen, cross_prob, mut_prob)
for i, f, s in result:

    if verbose:
        print("Generation number: {}, best value: {}\nBest solution: {}"
              .format(i, f, s))

    else:
        print("Generation number: {}, best value: {}"
              .format(i, f))
