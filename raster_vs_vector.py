import numpy as np
import matplotlib.pyplot as plt

n = 10**4

x = np.random.normal(size=n)
y = np.random.normal(size=n)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3))
color = np.array([0.6, 0.2, 0.7])

ax1.axis("equal")
ax2.axis("equal")

ax1.scatter(x, y, rasterized=True, color=color, edgecolor=color * 0.5)
ax2.scatter(x, y, rasterized=False, color=color, edgecolor=color * 0.5)

ax1.set_xlabel("x")
ax2.set_xlabel("x")

ax1.set_ylabel("y")
ax2.set_ylabel("y")


ax1.set_title("Rasterized")
ax2.set_title("Vector")

plt.tight_layout()

plt.savefig(f"rasterized_vs_vectorized_{n}.pdf")
plt.savefig(f"rasterized_vs_vectorized_{n}.png")

plt.close()
