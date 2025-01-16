import matplotlib.pyplot as plt
import numpy as np
import time

# Activer le mode interactif
plt.ion()

# Initialisation des paramètres
x = np.linspace(0, 2 * np.pi, 100)  # Axe des x
y1 = np.sin(x)  # Valeurs initiales pour le premier graphe
y2 = np.cos(x)  # Valeurs initiales pour le second graphe

# Création de la figure et des subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
line1, = ax1.plot(x, y1, label="sin(x)")
line2, = ax2.plot(x, y2, label="cos(x)")

# Paramètres des axes
ax1.set_title("Sinus en temps réel")
ax1.set_xlim(0, 2 * np.pi)
ax1.set_ylim(-1.5, 1.5)
ax1.legend()

ax2.set_title("Cosinus en temps réel")
ax2.set_xlim(0, 2 * np.pi)
ax2.set_ylim(-1.5, 1.5)
ax2.legend()

plt.tight_layout()

# Boucle de mise à jour
for i in range(100):
    y1 = np.sin(x + i * 0.1)  # Mise à jour des données sinus
    y2 = np.cos(x + i * 0.1)  # Mise à jour des données cosinus

    # Mise à jour des lignes
    line1.set_ydata(y1)
    line2.set_ydata(y2)

    # Redessiner la figure
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Pause pour simuler un délai en temps réel
    time.sleep(1/60)

# Désactiver le mode interactif
plt.ioff()
plt.show()
