import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,10,10000000)
y = np.random.random(10000000)
s1 = plt.plot(x, y)

plt.show()
