import numpy as np
import imported2 as M2

# tracks the knight's path
def knightMovement(parents):
    knightMoves = []

    for i in parents:
        tempList = []
        for j in range(0, len(i), 3):
            tempList.append([x + y for x, y in zip(knight, moves[i[j:j+3]])])
        knightMoves.append(tempList)

    return knightMoves

# checks if knight moves out of the board
def outOfBoard(coordinte):
    if coordinte[0] < 0 or coordinte[0] > 7 or coordinte[1] < 0 or coordinte[1] > 7:
        return True

    return False

# defining fitness function
def calculateFitness(parents):
    fitnessValues = []

    knightMoves = knightMovement(parents)

    for i in knightMoves:
        travelled = 0
        for j in range(len(i)):
            if i[j] in i[:j] or outOfBoard(i[j]):
                break
                
            travelled += 1

        fitnessValues.append(travelled)

    return fitnessValues

# the main loop
def step(parents, fitnessValues, mut_prob, cross_prob):
    newParents, f_newParents = M2.pselection(parents, fitnessValues, popSize, 2)
    children = M2.crossover(newParents)
    children = M2.mutation(children, mut_prob)
    newFitnessValues = calculateFitness(children)
    newChildren, fitnesses = M2.survivor_selection(parents, children, fitnessValues, newFitnessValues)

    return newChildren, fitnesses

# initialise starting position of knight
x = 3
y = 3
knight = [x, y]

# initialising hyper-parameters
popSize = 100
genSize = 1000
mut_prob = 0.3
cross_prob = 0.9

# assigning binary values to move numbers
binaryValues = {
1: "000",
2: "001",
3: "010",
4: "011",
5: "100",
6: "101",
7: "110",
8: "111"
}

# assigning direction to the binary values
moves = {
"000": [1, 2],
"001": [2, 1],
"010": [2,-1],
"011": [1, -2],
"100": [-1, -2],
"101": [-2, -1],
"110": [-2, 1],
"111": [-1, 2]
}

# initialising random population
movesInit = np.random.uniform(1, 9, size=(popSize, 30)).astype(int)

parents = []

# converting numpy array to list of strings
for i in movesInit:
    tempString = ""
    for j in i:
        tempString += binaryValues[j]

    parents.append(tempString)

fitnessValues = calculateFitness(parents)

# print(len(parents[0]))
# print(knightMovement(parents))
# print(fitnessValues)

populations = []
populations.append
bestFitness = [max(fitnessValues)]

for i in range(genSize):
  if i % int(genSize * 0.1) == 0:
    print('Generation: {}, best fitness: {:.2f}'.format(i, max(fitnessValues)))
  parents, fitnessValues = step(parents, fitnessValues, mut_prob, cross_prob)
  populations.append(parents)
  if max(fitnessValues) > bestFitness[-1]:
    bestFitness.append(max(fitnessValues))
  else:
    bestFitness.append(bestFitness[-1])
print('FINISHED!')