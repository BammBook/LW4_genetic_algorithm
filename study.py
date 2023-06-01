import random

from deap import creator, base, tools

ONE_MAX_LENGTH = 100
POPULATION_SIZE = 200
P_CROSSOVER = 0.9
P_MUTATION = 0.1
MAX_GENERATION = 50

# RANDOM_SEED = 42
# random.seed(RANDOM_SEED)


def zeroOrOne():
    return random.randint(0, 1)

def oneMaxFitness(individual):
    return sum(individual),

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

ind = creator.Individual

#
# def sum_of_two(a, b):
#     return a + b
#
#
toolbox = base.Toolbox()
# toolbox.register("incrementByFive", sum_of_two, b=5)
#
# print(toolbox.incrementByFive(100))

toolbox.register("zeroOrOne", random.randint, 0, 1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxOnePoint)
# toolbox.register("mutate", tools.mutUniformInt, low=-4000, up=4000, indpb=1 / LENGTH)
# toolbox.register("action", base_action)
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGTH)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)
toolbox.register("evaluate", oneMaxFitness)

# print(toolbox.mutate([1, 2, 3, 4, 5, 6]))
# randomList = tools.initRepeat(list, toolbox.action, LENGTH)
# print(randomList)
#
# print(max_profit())


population = toolbox.populationCreator(n=POPULATION_SIZE)
generation_counter = 0

fitness_values = list(map(toolbox.evaluate, population))
# print(len(fitness_values))
# print(fitness_values)
# print(population)
for individual, fitness_values in zip(population, fitness_values):
    individual.fitness.value = fitness_values
# print(population[0].fitness.values[0])
# print(population[0].fitness.values[0])
fitness_values = [individual.fitness.value for individual in population]
print(fitness_values)
print(len(fitness_values))
max_fitness_values = []
mean_fitness_values = []

while generation_counter < MAX_GENERATION:
    generation_counter += 1

    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    # mutation

    fresh_individuals = [ind for ind in offspring if not ind.fitness.valid]
    fresh_fitness_values = list(map(toolbox.evaluate, fresh_individuals))
    for individual, fitness_values in zip(fresh_individuals, fresh_fitness_values):
        individual.fitness.values = fitness_values

    population[:] = offspring

    fitness_values = [ind.fitness.values[0] for ind in population]

    max_fitness = max(fitness_values)
    mean_fitness = sum(fitness_values) / len(population)
    max_fitness_values.append(max_fitness)
    mean_fitness_values.append(mean_fitness)
    print("- Покорление {}: Макс. приспособ. = {}, средняя приспособ. = {}".format(generation_counter, max_fitness, mean_fitness))

    best_index = fitness_values.index(max(fitness_values))
    print("Лучший индивидуум = ", *population[best_index], "\n")
