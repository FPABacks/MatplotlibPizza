import numpy as np
import matplotlib
# Optional: Ensure right backend is in use. I like using Qt5Agg
# matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
print(f"You are using the {matplotlib.get_backend()} backend.")
from matplotlib.widgets import RectangleSelector
import matplotlib.animation as animation
# Extra scripts
from ruler import Ruler
from anatomy_figure import AnatomyFigure
import simple_nbody_sim as sns
from random_figure_generator import make_random_figure
from interactive_line_profiles import InteractivePlot

LATEX = False

# Lazy global fontsize for text on "normal" slides.
fs = 30

plt.rc("xtick", labelsize=15)
plt.rc("ytick", labelsize=15)
plt.rc("font", size=20)

# Check matplotlib version
mpl_version = matplotlib.__version__
min_version = "3.4.0"

for have, need in zip(mpl_version.split("."), min_version.split(".")):
    # The version is new, so (probably) fine
    if int(have) > int(need):
        break
    elif int(have) < int(need):
        print("Please install a more recent version of matplotlib")
        print(f"Installed version: {mpl_version}, at least required version: {min_version}")
        exit()


class ThePresentation:

    def __init__(self, start_slide=0, allow_latex=True):

        """
        Initialize the figure and all corresponding required widgets
        """
        self.current_slide = start_slide
        self.allow_latex = allow_latex
        self.step = 0
        self.latex = False
        self.serif = False
        self.fig = plt.figure(figsize=(16, 9))  # Typical screen aspect ratio.
        self.switch_latex()
        self.switch_serif()
        self.ax = None
        self.dark_theme = False

        # The particles in the N-body animation. First entry is a dummy point
        objects = np.array([[10**10, 0.35, 0.65],    # x
                            [10**10, 0.5, 0.5],      # y
                            [0, 0, 0],               # vx
                            [0, 0.00005, -0.00005],  # vy
                            [1e-10, 100, 100]])      # mass

        # The functions for each "slide" in a dictionary, waiting to be called.
        self.slide_dict = {0: self.title_slide,
                           1: self.basics_slide,
                           2: self.figsize_slide,
                           3: self.subplots_slide,
                           4: self.subplots_slide2,
                           5: self.slider_slide,
                           6: self.more_tips_slide,
                           7: self.histogram_example_slide,
                           8: self.vector_vs_raster,}

        # Some slides use some extra info that is nice to store
        self.slide_info = {0: objects,
                           1: (),
                           2: (),
                           3: 0,
                           4: 0,
                           5: (),
                           6: 0,
                           7: [[], [], []],
                           8: 0,}

        # OPTIONAL: Have n bodies rotating in a orbit together.
        # n_points = 3
        # angles = np.linspace(0, np.pi * 2, n_points, endpoint=False)
        # x = np.cos(angles) * 0.25 + 0.5
        # y = np.sin(angles) * 0.25 + 0.5
        # vx = np.sin(angles) * 0.00009
        # vy = -np.cos(angles) * 0.00009
        # m = np.ones(n_points) * 100

        # Connect the different key presses
        self.fig.canvas.mpl_connect('key_press_event', self.on_press)

        # Changes the speed (and accuracy) of the animation
        self.anim_dt = 0.5
        self.slide_dict[self.current_slide]()

        plt.show()

    def on_press(self, event):
        """
        Applies the action related to the pressed key.
        :param event: A matplotlib keypress widget event
        :return: nothing
        """
        print(f"Pressed key: {event.key}")
        if event.key == "e":
            self.switch_latex()
        elif event.key == "w":
            self.switch_serif()
        elif event.key == "r":
            self.redraw_figure()
        elif event.key == "right":
            self.step = 0
            self.stop_animation()
            if self.slide_dict[self.current_slide] == self.title_slide:
                self.fig.canvas.mpl_disconnect(self.grav_click)
            # elif self.slide_dict[self.current_slide - 1] == self.subplots_slide:
            try:
                self.fig.canvas.mpl_disconnect(self.ax_selector)
            except AttributeError:
                print("Nothing to disconnect!")

            self.current_slide += 1
            self.fig.clf()
            self.slide_dict[self.current_slide]()

            # These lines make sure the new things are drawn on the slide after a change.
            # These lines will appear many times
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        elif event.key == "left":
            if self.current_slide > 0:
                self.step = 0
                self.stop_animation()

                if self.slide_dict[self.current_slide] == self.title_slide:
                    self.fig.canvas.mpl_disconnect(self.grav_click)
                # elif self.slide_dict[self.current_slide + 1] == self.subplots_slide:
                try:
                    self.fig.canvas.mpl_disconnect(self.ax_selector)
                except AttributeError:
                    print("Nothing to disconnect!")

                self.fig.clf()
                self.current_slide -= 1
                self.slide_dict[self.current_slide]()

                self.fig.canvas.draw()
                self.fig.canvas.flush_events()

        elif event.key == " ":
            self.next_step()
        elif event.key == "z":
            self.ruler = Ruler(self.fig)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        elif event.key == "d":
            if self.dark_theme:
                plt.style.use("default")
                self.fig.set_facecolor("white")
            else:
                plt.style.use("dark_background")
                self.fig.set_facecolor("k")

            self.dark_theme = not self.dark_theme
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def stop_animation(self):
        """
        Lazy animation stopper. Only works if the animation is saved on self.ani of course.
        Exception to prevent crashes if no ani has been defined.
        """
        try:  # Lazy any animation stop in case there is an animation running.
            self.ani.event_source.stop()
        except AttributeError:
            pass

    def next_step(self):
        """
        Does an animation or update on a given slide.
        :return:
        """
        self.step += 1
        if self.slide_dict[self.current_slide] == self.basics_slide:
            if self.step == 1:
                self.anafig.add_basics()
            elif self.step == 2:
                self.anafig.add_labels_and_title()
            elif self.step == 3:
                self.anafig.add_ticks()
            elif self.step == 4:
                self.anafig.add_technical_points()
        elif self.slide_dict[self.current_slide] == self.figsize_slide:
            if self.step == 1:
                self.ruler = Ruler(self.fig)
        elif self.slide_dict[self.current_slide] == self.histogram_example_slide:
            if self.step == 1:
                self.update_hist1()
            elif self.step == 2:
                self.update_hist2()
            elif self.step == 3:
                self.update_hist3()
            elif self.step == 4:
                self.update_hist4()
            elif self.step == 5:
                self.update_hist5()
            elif self.step == 6:
                self.update_hist6()
            elif self.step == 7:
                self.update_hist7()
            elif self.step == 8:
                self.update_hist8()
            elif self.step == 9:
                self.update_hist9()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def redraw_figure(self):
        """
        Completely wipes the figure and redraws it from scratch.
        :return:
        """
        print(f"Redrawing slide number: {self.current_slide}")
        print(f"Using LateX: {self.latex}")
        print(f"Using serif fonts: {self.serif}")
        plt.clf()
        self.slide_dict[self.current_slide]()

    def switch_latex(self):
        """
        Switches between using LateX text rendering and default matplotlib rendering.
        :return:
        """
        self.latex = not self.latex

        print("Allow latex?:", self.allow_latex)
        if self.latex and self.allow_latex:
            plt.rcParams['text.usetex'] = self.latex
            print(f"Using Latex: {self.latex}")
        elif self.allow_latex:
            plt.rcParams['text.usetex'] = self.latex
            print(f"Using Latex: {self.latex}")
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def switch_serif(self):
        """
        Switches between serif and sans-serif fonts
        :return:
        """
        self.serif = not self.serif
        if self.serif:
            plt.rcParams["font.family"] = "Serif"
        else:
            plt.rcParams["font.family"] = "Sans-Serif"

        print(f"Using Serif: {self.serif}")

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def title_slide(self):
        """
        Just the title slide
        :return:
        """
        self.ax = plt.subplot(1, 1, 1)
        self.ax.text(0.5, 0.85, "Matplotlib, why it is pretty decent", fontsize=25,
                     transform=self.ax.transAxes, ha="center")
        self.fig.subplots_adjust(0.0, 0.0, 1, 1)

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.ax.set_xlim(-8/9 + 0.5, 8/9. + 0.5)
        self.ax.set_ylim(0, 1)

        # Connect widget to the function that adds the new points to the N-body
        self.grav_click = self.fig.canvas.mpl_connect('button_press_event', self.onclick_grav)

        self.scatter_points = []
        for i in range(len(self.slide_info[self.current_slide][0])):
            x = self.slide_info[self.current_slide][0, i]
            y = self.slide_info[self.current_slide][1, i]
            print(x, y)
            color = np.random.random(size=3)
            self.scatter_points.append(self.ax.scatter(x, y, color=color, edgecolor=color * 0.5, s=500,
                                                       linewidths=3, clip_on=True))

        # These lines make sure the new things are drawn on the slide.
        # In this case these might not be doing anything because the animation is now running from the start
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # Start the animation
        self.ani = animation.FuncAnimation(self.fig, self.animate_grav, interval=1, blit=True)

    def onclick_grav(self, event):
        """
        Add a body to the N-body simulator
        :param event:
        :return:
        """
        toolbar = plt.get_current_fig_manager().toolbar
        if event.button == 1 and toolbar.mode == "" and event.key != "shift" and event.inaxes == self.ax:
            x = event.xdata
            y = event.ydata
            vx = np.random.uniform(-0.0002, 0.0002)
            vy = np.random.uniform(-0.0002, 0.0002)
            m = 100
            objects = np.concatenate((self.slide_info[self.current_slide],
                                       [[x], [y], [vx], [vy], [m]]), axis=1)
            self.slide_info[self.current_slide] = objects

            color = np.random.random(size=3)

            self.scatter_points.append(self.ax.scatter(x, y, color=color, edgecolor=color * 0.5, s=500,
                                                       linewidths=3, clip_on=True))

    def animate_grav(self, t):
        """
        calculates the next step in the animation.
        :return:
        """
        indices = []
        # Update locations, only if there are points to show. (There is one dummy point)
        if len(self.slide_info[self.current_slide][0]) > 1:
            for i in range(50):  # Integrate 50 steps before drawing the new location of the points.
                self.slide_info[self.current_slide] = sns.rk4(self.slide_info[self.current_slide], self.anim_dt)

            # Select points that are still to be kept (runaway points are deleted)
            sel = ((self.slide_info[self.current_slide][0] < 10) *
                   (self.slide_info[self.current_slide][0] > -10) *
                   (self.slide_info[self.current_slide][1] < 10) *
                   (self.slide_info[self.current_slide][1] > -10))
            sel[0] = True
            self.slide_info[self.current_slide] = self.slide_info[self.current_slide][:, sel]
            indices = np.where(np.logical_not(sel))[0]

        # Remove points that have escaped. In inverse order to not mess up because of pop.
        for i in sorted(indices)[::-1]:
            self.scatter_points[i].remove()  # Removes the scatter point
            self.scatter_points.pop(i)  # Removes the left over None

        # Update plotted locations
        for i, point in enumerate(self.scatter_points):
            point.set_offsets(self.slide_info[self.current_slide][:2,i])

        return self.scatter_points

    def basics_slide(self):
        """
        Summarizes some of the basics
        :return:
        """
        if self.latex:
            self.switch_latex()
        if self.serif:
            self.switch_serif()

        self.fig.text(0.5, 0.9, r"The basics of Matplotlib figures", ha="center", va="center", fontsize=50)

        self.fig.text(0.075, 0.7, r"It is important to know what parts", fontsize=fs, ha="left")
        self.fig.text(0.075, 0.65, r"parts of a figure are called.", fontsize=fs, ha="left")
        self.fig.text(0.075, 0.5, r"Then you know what to search to", fontsize=fs, ha="left")
        self.fig.text(0.075, 0.45, r"fix them.", fontsize=fs, ha="left")

        self.ax = self.fig.add_subplot(1, 1, 1, aspect=1)
        self.fig.subplots_adjust(0.6, 0.2, 0.9, 0.8)

        self.anafig = AnatomyFigure(self.fig, self.ax)

    def figsize_slide(self):
        """
        Shows how the size of a figure works.
        :return:
        """
        if not self.latex:
            self.switch_latex()
        # if self.serif:
        #     self.switch_serif()

        # include the ruler
        self.ruler = Ruler(self.fig)

        # self.ax.text(0.1, 0.7, r"\texttt{figsize=(<Width>, <Height>)}", transform=self.ax.transAxes, fontsize=40)
        self.fig.text(0.5, 0.85, r"\texttt{figsize=(<Width>, <Height>)}", fontsize=fs * 1.5, zorder=-1, ha="center")
        self.fig.text(0.1, 0.75, r"Units are in inches", fontsize=fs, zorder=-1)
        self.fig.text(0.1, 0.65, r"Tip: Don't go too big!", fontsize=fs, zorder=-1)
        # self.fig.text(0.15, 0.63, r"Increase the DPI if you need a higher resolution", fontsize=fs, zorder=-1)
        self.fig.text(0.15, 0.55, r"\texttt{figsize=(20,20)} $\rightarrow 50 \times 50$\, cm!",
                      fontsize=fs, zorder=-1)
        self.fig.text(0.1, 0.45, r"My rough rule of thumb: About twice the size you want it to be on paper",
                      fontsize=fs, zorder=-1)
        self.fig.text(0.1, 0.35, r"The default widths of lines and sizes of fonts then seem to make the most sense",
                      fontsize=fs, zorder=-1)
        self.fig.text(0.1, 0.25, r"Alternatively set new defaults to work with you preferences",
                      fontsize=fs, zorder=-1)
        self.fig.text(0.1, 0.15, r"This can be done in the runtime configuration file (\texttt{matplotlibrc})",
                      fontsize=fs, zorder=-1)

    def subplots_slide(self):
        """
        Slide that allows drawing in subpplots
        :return:
        """
        self.ruler = Ruler(self.fig)

        # A bit of code that allows you to draw in new Axes
        self.fig_ax = self.fig.add_axes([0, 0, 1, 1], zorder=100)
        self.fig_ax.set_xlim(0, 1)
        self.fig_ax.set_ylim(0, 1)
        self.fig_ax.patch.set_alpha(0)

        self.ax_selector = RectangleSelector(self.fig_ax, self.add_axes, button=1)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def add_axes(self, eclick, erelease):
        """
        Adds axes in the selected rectangle
        :param eclick:
        :param erelease:
        :return:
        """
        if self.slide_dict[self.current_slide] == self.subplots_slide:

            # Get location of the drawn box
            x0 = min(eclick.xdata, erelease.xdata)
            width = max(eclick.xdata, erelease.xdata) - x0
            y0 = min(eclick.ydata, erelease.ydata)
            height = max(eclick.ydata, erelease.ydata) - y0

            # Create a new axes for the box
            new_ax = self.fig.add_axes([x0, y0, width, height])

            # Fill the axes with some random figure
            make_random_figure(new_ax, self.slide_info[self.current_slide])

            self.slide_info[self.current_slide] += 1

    def subplots_slide2(self):
        """
        The slide with the actual informative subplots information
        :return:
        """

        if not self.latex:
            self.switch_latex()

        self.fig.text(0.5, 0.9, r"Normal ways of making subplots",
                      fontsize=fs * 1.3, ha="center", va="center")

        self.fig.text(0.075, 0.75, r"\texttt{fig, axarr = plt.subplots(nrows, ncols, figsize=(ncols * 2, nrows * 2))}",
                      ha="left", fontsize=fs)
        self.fig.text(0.075, 0.65, r"\texttt{fig, ((ax11, ax12, ..), (ax21, ax22, ...) ...) = ...}",
                      ha="left", fontsize=fs)

        self.fig.text(0.075, 0.55, r"\texttt{ax = plt.subplot(row, col, index)}",
                      ha="left", fontsize=fs)

        self.fig.text(0.075, 0.45, r"\texttt{ax = fig.add_axes([x0, y0, width, height])}",
                      ha="left", fontsize=fs)

        self.fig.text(0.075, 0.35, r"many additional arguments available, e.g.: ",
                      fontsize=fs, ha="left")
        self.fig.text(0.15, 0.25, r"\texttt{aspect=..., sharex=..., sharey=..., projection=...}",
                      fontsize=fs, ha="left")

        self.fig.text(0.075, 0.15, r"For complex constructions use \texttt{GridSpec}",
                      fontsize=fs, ha="left")

    def vector_vs_raster(self):
        """
        Info about vector vs raster format.
        :return:
        """
        if not self.latex:
            self.switch_latex()
        if self.serif:
            self.switch_serif()

        self.fig.text(0.5, 0.9, r"Saving figures: Vectors vs Rasters",
                      fontsize=fs * 1.3, ha="center")

        self.fig.text(0.075, 0.75, r"Vector: PDF, PS, SVG",
                      ha="left", fontsize=fs)
        self.fig.text(0.075, 0.65, r"Raster: PNG, JPEG, TIFF",
                      ha="left", fontsize=fs)

        self.fig.text(0.075, 0.55, r"In general use vector format, it is scalable and looks better",
                      ha="left", fontsize=fs)
        self.fig.text(0.075, 0.45, r"If rasterized is required mind your DPI $\rightarrow$ 150 -- 300",
                      ha="left", fontsize=fs)
        self.fig.text(0.075, 0.35, r"Vector format figures can be both rasterized and vectorized",
                      ha="left", fontsize=fs)
        self.fig.text(0.075, 0.25, r"For example \texttt{ax.scatter(x, y, rasterized=True)}",
                      ha="left", fontsize=fs)

    def more_tips_slide(self):
        """
        Some tips and tricks
        :return:
        """
        if not self.latex:
            self.switch_latex()

        self.fig.text(0.5, 0.9, "Some things to consider", ha="center", fontsize=fs * 1.3)
        self.fig.text(0.075, 0.8, "Carefully choose your colors. Check for example ColorBrewer.", ha="left", fontsize=fs)
        self.fig.text(0.075, 0.7, r"Experiment with transparency, \texttt{alpha}.", ha="left", fontsize=fs)
        self.fig.text(0.075, 0.6, r"Experiment with line styles", ha="left", fontsize=fs)
        self.fig.text(0.075, 0.5, r"Experiment with borders and outlines, e.g. \texttt{edgecolor}", ha="left", fontsize=fs)
        self.fig.text(0.075, 0.4, r"Experiment with background lines that guide the eye", ha="left", fontsize=fs)
        self.fig.text(0.075, 0.3, r"Set the \texttt{zorder} of elements in your figure", fontsize=fs)
        self.fig.text(0.075, 0.2, r"But be consistent! Make the style mean the same thing.", fontsize=fs)

    def histogram_example_slide(self):
        """
        Generates random data for 3 histograms. Then plots them on three subplots.
        Starting very basic.
        :return:
        """
        if self.serif:
            self.switch_serif()
        if not self.latex:
            self.switch_latex()

        self.fig.text(0.35, 0.9, r"A little example ", fontsize=fs * 1.3, ha="center")
        self.fig.text(0.075, 0.8, r"\texttt{ax.hist(data)}", ha="left", fontsize=fs)

        data1 = np.random.normal(5, 0.5, size=100)
        data2 = np.random.normal(4, 1.5, size=3500)
        data3 = np.concatenate((np.random.normal(3, 0.8, size=250), np.random.normal(6, 2, size=1000)))

        # Save the data for later use.
        self.slide_info[self.current_slide][0] = [data1, data2, data3]

        # Kinda ugly way to hack the subplots in.
        ax1 = self.fig.add_axes([0.65, 0.70, 0.25, 0.25])
        ax2 = self.fig.add_axes([0.65, 0.40, 0.25, 0.25])
        ax3 = self.fig.add_axes([0.65, 0.10, 0.25, 0.25])

        # Save the axes and something that is a half decent choice for binning.
        self.slide_info[self.current_slide][1] = [ax1, ax2, ax3]
        self.slide_info[self.current_slide][2] = np.linspace(np.min(np.concatenate([data1, data2, data3])),
                                                             np.max(np.concatenate([data1, data2, data3])),
                                                             30)

        ax1.hist(data1)
        ax2.hist(data2)
        ax3.hist(data3 )

        ax1.set_ylabel("Number")
        ax2.set_ylabel("Number")
        ax3.set_ylabel("Number")

        ax3.set_xlabel("Size of pancakes [m$^2$]")

    def update_hist1(self):
        """
        It would be good to put them on the same scales.
        :return:
        """
        self.fig.text(0.075, 0.72, r"\texttt{..., sharex='all', sharey='all', ...}",
                      ha="left", fontsize=fs)

        ax1, ax2, ax3 = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]
        ax1.remove()
        ax2.remove()
        ax3.remove()

        ax1 = self.fig.add_axes([0.65, 0.70, 0.25, 0.25])
        ax2 = self.fig.add_axes([0.65, 0.40, 0.25, 0.25], sharex=ax1, sharey=ax1)
        ax3 = self.fig.add_axes([0.65, 0.10, 0.25, 0.25], sharex=ax2, sharey=ax2)

        ax1.hist(data1)
        ax2.hist(data2)
        ax3.hist(data3)

        ax1.set_ylabel("Number")
        ax2.set_ylabel("Number")
        ax3.set_ylabel("Number")

        ax3.set_xlabel("Size of pancakes [m$^2$]")
        self.slide_info[self.current_slide][1] = [ax1, ax2, ax3]

    def update_hist2(self):
        """
        Maybe it would be nice to normalize the histograms to a surface of 1.
        :return:
        """
        self.fig.text(0.075, 0.64, r"\texttt{ax.hist(data, density=True)}",
                      ha="left", fontsize=fs)

        ax1, ax2, ax3 = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]
        ax1.remove()
        ax2.remove()
        ax3.remove()

        ax1 = self.fig.add_axes([0.65, 0.70, 0.25, 0.25])
        ax2 = self.fig.add_axes([0.65, 0.40, 0.25, 0.25], sharex=ax1, sharey=ax1)
        ax3 = self.fig.add_axes([0.65, 0.10, 0.25, 0.25], sharex=ax2, sharey=ax2)

        ax1.hist(data1, density=True)
        ax2.hist(data2, density=True)
        ax3.hist(data3, density=True)

        ax1.set_ylabel("Density")
        ax2.set_ylabel("Density")
        ax3.set_ylabel("Density")

        ax3.set_xlabel("Size of pancakes")
        self.slide_info[self.current_slide][1] = [ax1, ax2, ax3]


    def update_hist3(self):
        """
        Maybe it would help if they all used the same binning
        :return:
        """
        self.fig.text(0.075, 0.56, r"\texttt{+ bins=something_decent}",
                      ha="left", fontsize=fs)

        ax1, ax2, ax3 = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]
        ax1.remove()
        ax2.remove()
        ax3.remove()

        ax1 = self.fig.add_axes([0.65, 0.70, 0.25, 0.25])
        ax2 = self.fig.add_axes([0.65, 0.40, 0.25, 0.25], sharex=ax1, sharey=ax1)
        ax3 = self.fig.add_axes([0.65, 0.10, 0.25, 0.25], sharex=ax2, sharey=ax2)

        decent_bins = self.slide_info[self.current_slide][2]
        ax1.hist(data1, density=True, bins=decent_bins)
        ax2.hist(data2, density=True, bins=decent_bins)
        ax3.hist(data3, density=True, bins=decent_bins)

        ax1.set_ylabel("Density")
        ax2.set_ylabel("Density")
        ax3.set_ylabel("Density")

        ax3.set_xlabel("Size of pancakes [m$^2$]")
        self.slide_info[self.current_slide][1] = [ax1, ax2, ax3]

    def update_hist4(self):
        """
        It would probably make sense to plot the histograms in the same subplot.
        :return:
        """

        ax1, ax2, ax3 = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]

        ax1.remove()
        ax2.remove()
        ax3.remove()

        ax1 = self.fig.add_axes([0.65, 0.25, 0.30, 0.50])

        decent_bins = self.slide_info[self.current_slide][2]
        ax1.hist(data1, density=True, bins=decent_bins, label="Data 1")
        ax1.hist(data2, density=True, bins=decent_bins, label="Data 2")
        ax1.hist(data3, density=True, bins=decent_bins, label="Data 3")

        ax1.legend()

        ax1.set_ylabel("Density")
        ax1.set_xlabel("Size of pancakes [m$^2$]")

        self.slide_info[self.current_slide][1] = [ax1]

    def update_hist5(self):
        """
        Maybe a stepped histogram would be nice
        :return:
        """

        self.fig.text(0.075, 0.48, r"\texttt{ax.hist(..., histtype='step', ...)}",
                      ha="left", fontsize=fs)

        ax1, = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]

        ax1.remove()
        ax1 = self.fig.add_axes([0.65, 0.25, 0.30, 0.50])

        decent_bins = self.slide_info[self.current_slide][2]
        ax1.hist(data1, density=True, bins=decent_bins, label="Data 1",
                 histtype="step", lw=3)
        ax1.hist(data2, density=True, bins=decent_bins, label="Data 2",
                 histtype="step", lw=3)
        ax1.hist(data3, density=True, bins=decent_bins, label="Data 3",
                 histtype="step", lw=3)

        ax1.legend()

        ax1.set_ylabel("Density")
        ax1.set_xlabel("Size of pancakes [m$^2$]")

        self.slide_info[self.current_slide][1] = [ax1]

    def update_hist6(self):
        """
        A step filled histogram could be cool.
        :return:
        """
        self.fig.text(0.075, 0.40, r"\texttt{+ histtype='stepfilled', edgecolor='k', alpha=0.5,}",
                      ha="left", fontsize=fs)

        ax1, = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]

        ax1.remove()
        ax1 = self.fig.add_axes([0.65, 0.25, 0.30, 0.50])

        decent_bins = self.slide_info[self.current_slide][2]
        ax1.hist(data1, density=True, bins=decent_bins, label="Data 1",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5)
        ax1.hist(data2, density=True, bins=decent_bins, label="Data 2",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5)
        ax1.hist(data3, density=True, bins=decent_bins, label="Data 3",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5)



        ax1.legend()

        ax1.set_ylabel("Density")
        ax1.set_xlabel("Size of pancakes [m$^2$]")

        self.slide_info[self.current_slide][1] = [ax1]

    def update_hist7(self):
        """
        Maybe different colors are nicer?
        :return:
        """
        ax1, = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]

        ax1.remove()
        ax1 = self.fig.add_axes([0.65, 0.25, 0.30, 0.50])

        decent_bins = self.slide_info[self.current_slide][2]
        ax1.hist(data1, density=True, bins=decent_bins, label="Data 1",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5, color="#1b9e77")
        ax1.hist(data2, density=True, bins=decent_bins, label="Data 2",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5, color="#d95f02")
        ax1.hist(data3, density=True, bins=decent_bins, label="Data 3",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5, color="#7570b3")

        ax1.legend()

        ax1.set_ylabel("Density")
        ax1.set_xlabel("Size of pancakes [m$^2$]")

        self.slide_info[self.current_slide][1] = [ax1]

    def update_hist8(self):
        """
        Maybe a cumulative histogram would be nice?
        :return:
        """
        self.fig.text(0.075, 0.32, r"Or something like \texttt{ cumulative=True}", ha="left",
                      fontsize=fs)

        ax1, = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]

        ax1.remove()
        ax1 = self.fig.add_axes([0.65, 0.25, 0.30, 0.50])

        decent_bins = self.slide_info[self.current_slide][2]
        ax1.hist(data1, density=True, bins=decent_bins, label="Data 1",
                 histtype="step", lw=3, color="#1b9e77", cumulative=True)
        ax1.hist(data2, density=True, bins=decent_bins, label="Data 2",
                 histtype="step", lw=3, color="#d95f02", cumulative=True)
        ax1.hist(data3, density=True, bins=decent_bins, label="Data 3",
                 histtype="step", lw=3, color="#7570b3", cumulative=True)

        ax1.legend(loc="upper left")

        ax1.set_ylabel("Density")
        ax1.set_xlabel("Size of pancakes [m$^2$]")

        self.slide_info[self.current_slide][1] = [ax1]

    def update_hist9(self):
        """
        A sort of final version with all fonts the same and such.
        :return:
        """
        if not self.serif:
            self.switch_serif()

        ax1, = self.slide_info[self.current_slide][1]
        data1, data2, data3 = self.slide_info[self.current_slide][0]

        ax1.remove()
        ax1 = self.fig.add_axes([0.65, 0.25, 0.30, 0.50])

        decent_bins = self.slide_info[self.current_slide][2]
        ax1.hist(data1, density=True, bins=decent_bins, label="Data 1",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5, color="#1b9e77")
        ax1.hist(data2, density=True, bins=decent_bins, label="Data 2",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5, color="#d95f02")
        ax1.hist(data3, density=True, bins=decent_bins, label="Data 3",
                 histtype="stepfilled", lw=3, edgecolor="k", alpha=0.5, color="#7570b3")

        ax1.legend()

        ax1.set_ylabel("Density")
        ax1.set_xlabel("Size of pancakes [m$^2$]")

        self.slide_info[self.current_slide][1] = [ax1]

    def slider_slide(self):
        """
        Does stuff
        :return:
        """
        if self.latex:
            self.switch_latex()
        if self.serif:
            self.switch_serif()

        # Generate "line profiles"
        a = np.arange(1, 6, 1)
        b = np.arange(1, 6, 1)
        c = np.arange(1, 6, 1)
        d = np.arange(1, 6, 1)
        t = np.linspace(0, np.pi * 2, 600)

        param_vals = []
        line_profiles = []

        for ai in a:
            for bi in b:
                for ci in c:
                    for di in d:
                        param_vals.append([ai, bi, ci, di])
                        line_profiles.append([])
                        line_profiles[-1].append([t, np.cos(ai * t)])
                        line_profiles[-1].append([t, np.sin(bi * t)])
                        line_profiles[-1].append([t, np.cos(ci * t)])
                        line_profiles[-1].append([t, np.sin(di * t)])
                        line_profiles[-1].append([np.cos(ai * t) * np.sin(bi * t),
                                                  np.cos(ci * t) * np.sin(di * t)])

        param_vals = np.array(param_vals)
        line_profiles = np.array(line_profiles)

        line_names = [r"cos($at$)", r"sin($bt$)", r"cos($ct$)", r"sin($dt$)",
                      r"x = cos($at$) sin($bt$), y = cos($ct$)  sin($dt$)"]
        slider_plot = InteractivePlot(self.fig, line_profiles, param_vals,
                 ["a", "b", "c", "d"], [a, b, c, d], line_names)

        slider_plot.init_plot()


pres = ThePresentation(start_slide=0, allow_latex=LATEX)
