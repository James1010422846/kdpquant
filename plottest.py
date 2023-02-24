import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.5, 10, 1000)
y = np.cos(x)
plt.plot(x, y, ls='-', lw=2, label='cosine', color='purple')

plt.legend()
plt.xlabel('independent variable')
plt.ylabel('dependent variable')
plt.show()
