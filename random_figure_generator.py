import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal


def make_random_figure(ax, number_of_subplot):
    """
    Makes a believable figure of a random matplotlib axes, will generate (combinations of)
     scatter plots, line plots, histograms, and colormeshes.
    :param ax:
    :return:
    """
    # Randomlize the random seed just in case
    np.random.seed()
    fontsize = 15
    # First determine the type of plot
    types = ["colormesh", "scatter", "line", "scatter_and_line", "histogram", "line_profile"]
    type = types[number_of_subplot % len(types)]

    if type == "histogram":
        components = np.random.choice([2, 3, 4])

        ax.set_xlabel("Something measurable", fontsize=fontsize)
        ax.set_ylabel("Density", fontsize=fontsize)

        for i in range(components):
            n_points = np.random.randint(20, 10000)
            data = np.random.normal(np.random.uniform(-2, 2), np.random.uniform(0.2, 1.),
                                    size=n_points)
            ax.hist(data, bins=max(int(n_points**0.3333), 6),
                    color=np.concatenate([np.random.random(size=3), [0.5]]),
                    edgecolor="k", histtype="stepfilled", lw=2)

    elif type == "scatter":
        components = np.random.choice([3, 4, 5])

        ax.set_ylabel("Important parameter [tables]", fontsize=fontsize)
        ax.set_xlabel("Boring values [pineapples]", fontsize=fontsize)

        for i in range(components):
            n_points = np.random.randint(5, 100)

            marker = np.random.choice(["p", "s", ".", "o", "v", "x", "+", "d"])
            color = np.random.random(size=3)

            x = np.random.uniform(0.2, 3., n_points)
            y = np.random.uniform(0.3, 0.7) * x + np.random.normal(0, 0.2, size=n_points)

            ax.scatter(x, y, color=color, edgecolor=color * 0.5, marker=marker)

    elif type == "line":
        ax.set_xlabel("I don't know... Time or something [Dog years]", fontsize=fontsize)
        ax.set_ylabel(" Normalized hailstones fallen", fontsize=fontsize)

        n_points = 200
        x = np.linspace(0, 10, n_points)

        y1 = np.random.normal(size=n_points) * 0.2 + np.sin(x)
        y2 = 0.1 * x - 1 + np.sin(x + 3) * 0.5
        y3 = (x**1.2) % 3

        ax.plot(x, y1, c=np.random.random(3))
        ax.plot(x, y2, c=np.random.random(3))
        ax.plot(x, y3, c=np.random.random(3), ls="--")
        ax.axhline(1, ls="--", c="0.5")

    elif type == "scatter_and_line":

        coeffs = np.random.uniform(-1, 1, size=5) * np.array([1, 0.5, 0.1, 1e-2, 1e-3])[::-1]

        x = np.linspace(0, 5, 100)
        p = np.poly1d(coeffs)

        y = p(x)

        xscat = np.random.uniform(0, 5, 100)
        yscat = p(xscat) * (1 + np.random.normal(size=100))

        color = np.random.random(3)

        ax.plot(x, y, color=color)
        ax.scatter(xscat, yscat, color=color, alpha=0.5)

        ax.set_xlabel("Spam", fontsize=fontsize)
        ax.set_ylabel("Important stuff", fontsize=fontsize )

    elif type == "line_profile":

        min_wave, max_wave = 4560, 4570
        wave = np.linspace(min_wave, max_wave, 100)
        w0_1 = np.random.uniform(min_wave + 1, max_wave - 1)
        w0_2 = np.random.uniform(min_wave + 1, max_wave - 1)
        w0_3 = np.random.uniform(min_wave + 1, max_wave - 1)
        flux = 1 - (np.exp(-(wave - w0_1)**2 / 0.5) * 2 +
                    np.exp(-(wave - w0_2) ** 2 / 0.5) * 1.5 +
                    np.exp(-(wave - w0_3) ** 2 / 0.5))
        flux_with_noise = flux + np.random.normal(0, scale=0.1, size=100)

        ax.set_xlabel(r"Wavelength [$\rm{\AA}$]", fontsize=fontsize)
        ax.set_ylabel("Normalized flux", fontsize=fontsize)

        ax.plot(wave, flux_with_noise, c="purple")
        ax.plot(wave, flux, c="orange")
        ax.axhline(1, ls="--", c="0.5", lw=1)

    elif type == "colormesh":

        x_points = np.linspace(-np.pi, np.pi, 50)
        y_points = np.linspace(-np.pi, np.pi, 50)

        x_mesh, y_mesh = np.meshgrid(x_points, y_points)

        z_mesh = multivariate_normal.pdf(np.array([x_mesh.reshape(-1), y_mesh.reshape(-1)]).T, mean=np.array([0, 0]),
                                          cov=np.array([[1, -0.75], [0.75, 1]])).reshape(50,50) * x_mesh**2

        # z_mesh = np.sin(x_mesh) * np.cos(y_mesh)

        levels = np.linspace(np.min(z_mesh), np.max(z_mesh), 5)[1:-1]
        ax.pcolormesh(x_points, y_points, z_mesh)
        ax.contour(x_points, y_points, z_mesh, levels=levels, colors=["red"] * len(levels), zorder=100)

        ax.set_ylabel("Number of pancakes", fontsize=fontsize)
        ax.set_xlabel("The color Purple", fontsize=fontsize)

    ax.tick_params(axis="x", labelsize=1 * fontsize)
    ax.tick_params(axis="y", labelsize=1 * fontsize)

    return ax


if __name__ == "__main__":
    """
    A little test for the figures
    """
    # plt.rcParams["font.family"] = "serif"

    # Can also specify fonts directly, but they have to be available.
    # plt.rcParams["font.family"] = "Cambria Math"

    plt.rcParams["text.usetex"] = True

    number_figures = 6
    ncols = 3
    nrows = int(np.ceil(number_figures / ncols))
    fig, axarr = plt.subplots(nrows, ncols, figsize=(16,9))
    axarr = axarr.ravel()
    for i, ax in enumerate(axarr):
        make_random_figure(ax, i)

    plt.tight_layout()
    plt.show()