import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 100)

ax1 = plt.subplot(212)
ax1.plot(t, t)

ax2 = plt.subplot(221)
ax2.plot(t, np.sin(t))

ax3 = plt.subplot(222)
ax3.plot(t, np.cos(t))

plt.show()