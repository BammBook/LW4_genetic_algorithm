import random

import numpy as np
from deap import creator, base, tools
from matplotlib import pyplot as plt
from numpy import double

from ReadTest import ReadTest

LENGTH = 24
POPULATION_SIZE = 200
P_CROSSOVER = 0.9
P_MUTATION = 0.05
MAX_GENERATION = 50

MAX_ACT = 4

data = ReadTest('C:/Study/Optimization/LW4/TestData/test2')

capacity = data.capacity
init_charge = data.init_charge
price_schedule = data.price_schedule
load_schedule = data.load_schedule
constant_load = data.constant_load
target_charge = data.target_charge


def base_action(a=-MAX_ACT, b=MAX_ACT):
    return random.randint(a, b) * 1000


action = [base_action() for i in range(len(price_schedule))]


def max_profit(sell=action):
    profit = 0
    current_charge = init_charge
    for i in range(0, len(price_schedule)):
        current_charge = current_charge - constant_load - load_schedule[i] + sell[i]
        profit = profit - price_schedule[i] * sell[i]
        if current_charge < 0 or current_charge > capacity:
            profit = 0
            return (profit),

    return (profit),


# def max_profit(individual):
#     return sum(individual),


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


toolbox.register("select", tools.selTournament, k=200, tournsize=3)
toolbox.register("mate", tools.cxOnePoint)
# toolbox.register("mutate", tools.mutUniformInt, low=-4000, up=4000, indpb=1 / LENGTH)
toolbox.register("action", base_action)
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.action, LENGTH)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)
toolbox.register("evaluate", max_profit)

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
fitness_values = [individual.fitness.value for individual in population]

max_fitness_values = []
mean_fitness_values = []

while generation_counter < MAX_GENERATION:
    generation_counter += 1

    offspring = toolbox.select(population)
    offspring = list(map(toolbox.clone, offspring))
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    # mutation

    fresh_individuals = [ind for ind in offspring if not ind.fitness.valid]
    fresh_fitness_values = list(map(toolbox.evaluate, fresh_individuals))
    # fresh_fitness_values = list(map(toolbox.evaluate, population))

    for individual, fitness_values in zip(fresh_individuals, fresh_fitness_values):
        individual.fitness.values = fitness_values

    population[:] = offspring

    fitness_values = [ind.fitness.values[0] for ind in population]

    max_fitness = max(fitness_values)
    mean_fitness = sum(fitness_values) / len(population)
    max_fitness_values.append(max_fitness)
    mean_fitness_values.append(mean_fitness)
    print("- Покорление {}: Макс. приспособ. = {}, средняя приспособ. = {}".format(generation_counter, max_fitness,
                                                                                   mean_fitness))

    best_index = fitness_values.index(max(fitness_values))
    print("Лучший индивидуум = ", *population[best_index], "\n")



t = np.arange(1, len(data.load_schedule) + 1, 1)

load = [data.constant_load + data.load_schedule[i] for i in range(0, len(data.load_schedule))]
charge1 = [0.0] * len(load)
charge1[0] = data.init_charge - load[0]
for i in range(1, len(load)):
    charge1[i] = charge1[i - 1] - load[i]

# action = [double(random.randint(-4, 4) * 1000) for i in range(0, len(t))]
action = population[best_index]

colors = [''] * len(action)
for i in range(len(colors)):
    if action[i] >= 0:
        colors[i] = 'g'
    else:
        colors[i] = 'r'

charge2 = [0.0] * len(load)
charge2[0] = data.init_charge - load[0] + action[0]
for i in range(1, len(load)):
    charge2[i] = charge1[i - 1] - load[i] + action[i]

figure = plt.figure(figsize=(12, 7))
plt.suptitle('Operation process')

fig1 = plt.subplot(3, 1, 1)
plt.title('Charge of power storage')
plt.xlabel('Time')
fig1.grid(True)
fig1.plot(t, charge1, 'b', t, charge2, 'r')
fig1.legend(['without trading', 'with trading'])

fig2 = plt.subplot(3, 1, 2)
plt.title('Price of power')
plt.xlabel('Time')
fig2.grid(True)
fig2.plot(t, data.price_schedule, 'r')

fig3 = plt.subplot(3, 1, 3)
plt.title('Action')
plt.xlabel('Time')
fig3.bar(t, action, color=colors)

plt.show()
