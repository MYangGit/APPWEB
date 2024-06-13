import matplotlib.pyplot as plt
import numpy as np

# fig1, ax = plt.subplots()
# x = np.linspace(0, 10, 100)
# y = x
# l1, = ax.plot(x, y)

# fig, ax = plt.subplots()
# x = np.linspace(0, 10, 100)
# y = np.sin(x)
# l2, = ax.plot(x, y)

# fig, ax = plt.subplots()
# x = np.linspace(0, 10, 100)
# y1 = np.cos(x)
# y2 = np.sin(x)
# l3, l4 = ax.plot(x, y1, x, y2)

fig, ax = plt.subplots()
x = np.random.random(100)
y = np.random.random(100)
s1 = ax.scatter(x, y)

plt.show()
