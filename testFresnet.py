import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Définir la courbe (hélice)
t = np.linspace(0, 4 * np.pi, 100)
x = np.cos(t)
y = np.sin(t)
z = t
r = np.array([x, y, z]).T

# Calcul des dérivées
dr = np.gradient(r, axis=0)
d2r = np.gradient(dr, axis=0)

# Calcul des vecteurs Frenet
T = dr / np.linalg.norm(dr, axis=1)[:, None]  # Tangent
N = np.gradient(T, axis=0)
N = N / np.linalg.norm(N, axis=1)[:, None]  # Normalisé
B = np.cross(T, N)  # Binormal

# Visualisation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label="Courbe")
for i in range(0, len(t), 10):  # Intervalles réguliers
    ax.quiver(r[i, 0], r[i, 1], r[i, 2], T[i, 0], T[i, 1], T[i, 2], color='r', label="T" if i == 0 else "")
    ax.quiver(r[i, 0], r[i, 1], r[i, 2], N[i, 0], N[i, 1], N[i, 2], color='g', label="N" if i == 0 else "")
    ax.quiver(r[i, 0], r[i, 1], r[i, 2], B[i, 0], B[i, 1], B[i, 2], color='b', label="B" if i == 0 else "")

ax.legend()
plt.show()
