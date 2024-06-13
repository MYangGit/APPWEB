import matplotlib.pyplot as plt
import numpy as np

# 生成随机数据
x = np.random.rand(100)
y = np.random.rand(100)
colors = np.random.rand(100)
sizes = 1000 * np.random.rand(100)

# 绘制散点图
fig, ax = plt.subplots()
ax.scatter(x, y, c=colors, s=sizes, alpha=0.5)
s1 = ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Scatter Plot')

plt.show()