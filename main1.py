import numpy as np
from numpy import double
import matplotlib.pyplot as plt
import random

from ReadTest import ReadTest


def plot_graf(x, y, title=''):
    plt.figure()
    plt.title(title)
    plt.grid(True)
    # plt.axis(
    #     [1, len(t), np.sign(np.min(current_charge)) * 1.1 * np.abs(np.min(current_charge)), 1.1 * np.max(current_charge)])
    plt.plot(x, y)
    plt.show()



data = ReadTest('C:/Study/Optimization/LW4/TestData/test2')

t = np.arange(1, len(data.load_schedule) + 1, 1)

load = [data.constant_load + data.load_schedule[i] for i in range(0, len(data.load_schedule))]
charge1 = [0.0] * len(load)
charge1[0] = data.init_charge - load[0]
for i in range(1, len(load)):
    charge1[i] = charge1[i - 1] - load[i]

action = [double(random.randint(-4, 4) * 1000) for i in range(0, len(t))]

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

fig1 = plt.subplot(1, 3, 1)
plt.title('Charge of power storage')
plt.xlabel('Time')
fig1.grid(True)
fig1.plot(t, charge1, 'b', t, charge2, 'r')
fig1.legend(['without trading', 'with trading'])

fig2 = plt.subplot(1, 3, 2)
plt.title('Price of power')
plt.xlabel('Time')
fig2.grid(True)
fig2.plot(t, data.price_schedule, 'r')

fig3 = plt.subplot(1, 3, 3)
plt.title('Action')
plt.xlabel('Time')
fig3.bar(t, action, color=colors)

plt.show()
