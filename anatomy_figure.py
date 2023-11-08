# ----------------------------------------------------------------------------
# Title:   Scientific Visualisation - Python & Matplotlib
# Author:  Nicolas P. Rougier
# License: BSD
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
from matplotlib.patches import Circle
from matplotlib.patheffects import withStroke

class AnatomyFigure:

    def __init__(self, fig, ax):

        np.random.seed(123)

        X = np.linspace(0.5, 3.5, 100)
        Y1 = 3 + np.cos(X)
        Y2 = 1 + np.cos(1 + X / 0.75) / 2
        Y3 = np.random.uniform(Y1, Y2, len(X))

        self.fig = fig
        self.ax = ax

        self.ax.xaxis.set_major_locator(MultipleLocator(1.000))
        self.ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        self.ax.yaxis.set_major_locator(MultipleLocator(1.000))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(4))
        self.ax.xaxis.set_minor_formatter(FuncFormatter(self.minor_tick))

        self.ax.set_xlim(0, 4)
        self.ax.set_ylim(0, 4)

        self.ax.tick_params(which="major", width=1.0)
        self.ax.tick_params(which="major", length=10)
        self.ax.tick_params(which="minor", width=1.0, labelsize=10)
        self.ax.tick_params(which="minor", length=5, labelsize=10, labelcolor="0.25")

        self.ax.grid(linestyle="--", linewidth=0.5, color=".25", zorder=-10)

        self.ax.plot(X, Y1, c=(0.25, 0.25, 1.00), lw=2, label="Blue signal", zorder=10)
        self.ax.plot(X, Y2, c=(1.00, 0.25, 0.25), lw=2, label="Red signal")
        self.ax.plot(X, Y3, linewidth=0, marker="o", markerfacecolor="w", markeredgecolor="k")

        self.ax.set_title("Anatomy of a figure", fontsize=20, verticalalignment="bottom")
        self.ax.set_xlabel("X axis label")
        self.ax.set_ylabel("Y axis label")

        self.ax.legend(loc="upper right")

    def minor_tick(self, x, pos):
        if not x % 1.0:
            return ""
        return "%.2f" % x

    def circle(self,x, y, radius=0.15):

        circle = Circle(
                        (x, y),
                        radius,
                        clip_on=False,
                        zorder=10,
                        linewidth=1,
                        edgecolor="black",
                        facecolor=(0, 0, 0, 0.0125),
                        path_effects=[withStroke(linewidth=5, foreground="w")],
                        )
        self.ax.add_artist(circle)

    def text(self, x, y, text):
        self.ax.text(x,
                     y,
                     text,
                     backgroundcolor="white",
                     # fontname="Yanone Kaffeesatz", fontsize="large",
                     ha="center",
                     va="top",
                     weight="regular",
                     color="#000099",
                     zorder=100)

    def add_ticks(self):
        """
        Indicate the ticks
        :return:
        """
        # Minor tick
        self.circle(0.50, -0.10)
        self.text(0.50, -0.32, "Minor tick label")

        # Major tick
        self.circle(-0.03, 4.00)
        self.text(0.03, 3.80, "Major tick")

        # Minor tick
        self.circle(0.00, 3.50)
        self.text(0.00, 3.30, "Minor tick")

        # Major tick label
        self.circle(-0.15, 3.00)
        self.text(-0.15, 2.80, "Major tick label")

    def add_basics(self):
        # Blue plot
        self.circle(1.75, 2.80)
        self.text(1.75, 2.60, "Line\n(line plot)")

        # Red plot
        self.circle(1.20, 0.60)
        self.text(1.20, 0.40, "Line\n(line plot)")

        # Scatter plot
        self.circle(3.20, 1.75)
        self.text(3.20, 1.55, "Markers\n(scatter plot)")

    def add_labels_and_title(self):
        # X Label
        self.circle(1.80, -0.35)
        self.text(1.80, -0.55, "X axis label")

        # Y Label
        self.circle(-0.30, 1.80)
        self.text(-0.30, 1.6, "Y axis label")

        # Title
        self.circle(1.60, 4.13)
        self.text(1.60, 3.93, "Title")

        # Legend
        self.circle(3.70, 3.80)
        self.text(3.70, 3.60, "Legend")

    def add_technical_points(self):
        # Grid
        self.circle(3.00, 3.00)
        self.text(3.00, 2.80, "Grid")

        # Axes
        self.circle(0.5, 0.5)
        self.text(0.5, 0.3, "Axes")

        # Figure
        self.circle(-0.3, 0.65)
        self.text(-0.3, 0.45, "Figure")

        color = "#000099"
        self.ax.annotate(
            "Spines",
            xy=(4.0, 0.35),
            xytext=(3.3, 0.5),
            color=color,
            weight="regular",  # fontsize="large", fontname="Yanone Kaffeesatz",
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color=color),
        )

        self.ax.annotate(
            "",
            xy=(3.15, 0.0),
            xytext=(3.45, 0.45),
            color=color,
            weight="regular",  # fontsize="large", fontname="Yanone Kaffeesatz",
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color=color),
        )



















