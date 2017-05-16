from deap import base, creator
import random
from deap import tools, algorithms
from scipy.stats import bernoulli
import pdb

population_size = 10
num_generations = 5
L = 10

def evaluateModel(individual):
    return sum(individual),

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list , fitness = creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("binary", bernoulli.rvs, 0.5)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.binary, n = L)
toolbox.register("population", tools.initRepeat, list , toolbox.individual)

toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb = 0.8)
toolbox.register("select", tools.selRoulette)
toolbox.register("evaluate", evaluateModel)

popl = toolbox.population(n = population_size)
result = algorithms.eaSimple(popl, toolbox, cxpb = 0.4, mutpb = 0.01, ngen = num_generations, verbose = True)

best_individuals = tools.selBest(popl, k = 3)
for bi in best_individuals:
    print(bi)
