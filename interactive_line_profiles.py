"""
Plotting routine for interactive investigation of model grids showing spectroscopic line profiles.
By: Frank Backs
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons




class InteractivePlot:
    """
    Plots line profiles from a grid of models. Currently assumes the profiles are not yet convolved with
    rotational and resolution profiles. Adds vsini as an additional free parameter. Has slider buttons to change the
    value of each parameter. Additionally has buttons to show every model available given all but 1 parameter.
    The spacing of the plots, sliders and buttons is probably not very robust, probably causing issues if you have too
    many free parameters, too many lines, weird sized screens/screen settings. Play with the settings to fix that :)

    Note: An additional spectrum (model or observation) can be plotted when initializing the plot by including
    "extra_wave" and "extra_flux" and optionally "extra_error".
    """
    def __init__(self, fig, line_profiles, model_parameters,
                 parameter_names, unique_params, line_names, use_wave_range=False, ncols=5):
        """
        :param line_profiles:       Array with all lines profiles for each set of parameters and each line
                                    Shape: (N_models, N_lines, 2, N_wavelength_points)
        :param model_parameters:    Array with all model parameters, shape: (N_models, N_parameters)
        :param parameter_names:     List with the names of the varied parameters
        :param unique_params:       The unique values of each of the parameters
        :param line_names:          List of names of the lines to show must be same length as second dimension
                                    of line_profiles.
        :param line_dict:           A dictionary with line names matched to (resolution at the line, minwave, maxwave)
        :param use_wave_range:      Determines if the minwave and maxwave of line_dict are going to be used
                                    to determine the displayed range. Otherwise it will be determined using
        """

        self.line_profiles = line_profiles
        self.model_parameters = model_parameters
        self.parameter_names = list(parameter_names) #+ [r"$v \sin i$"]
        self.unique_params = unique_params
        self.line_names = line_names
        self.use_wave_range = use_wave_range
        self.param_dict = dict(zip(parameter_names, unique_params))

        # The lines as matplotlib defines them
        self.mpl_lines = []

        # Slider options
        self.length = 0.3
        self.width = 0.03
        self.h_space = 0.075
        self.v_space = 0.005
        self.slide_cols = 2
        self.slide_rows = len(self.parameter_names) // self.slide_cols +\
                          int((len(self.parameter_names) % self.slide_cols) > 0)
        self.slide_top = self.slide_rows * (self.v_space + self.width) + 0.035
        self.sliderAxes = []
        self.sliders = []
        self.fontsize = 20

        # parameters for the option of plotting multiple lines
        self.active_lines = 1
        self.max_models = np.max([len(up) for up in self.unique_params])

        # Initialize figure
        # self.figsize = (16, 9)
        self.fig = fig
        self.axarr = None
        # self.ncols = ncols
        # self.nrows = len(line_names) // self.ncols + int((len(line_names) % self.ncols) > 0)

        # Colormap defaults
        self.cmap = matplotlib.cm.viridis
        self.norm = matplotlib.colors.Normalize(0, 1)
        self.colormap = matplotlib.cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

        # Initialize radio buttons
        self.radio_buttons = None

    def init_sliders(self):
        """
        Makes the sliders
        :return:
        """
        for i, param_name in enumerate(self.parameter_names):
            # Get position of slider
            col = i % self.slide_cols
            row = i // self.slide_cols

            # Create an axis for each of the sliders
            ax = plt.axes([0.05 + col * (self.length + self.h_space),
                           self.slide_top - row * (self.v_space + self.width),
                           self.length,
                           self.width])

            # save the axes in case you need them
            self.sliderAxes.append(ax)

            # Create the sliders, exception for vsini
            if "sin i" in param_name:
                self.sliders.append(Slider(ax, param_name, 1, 300, valfmt="%i", fontsize=self.fontsize))
            else:
                self.sliders.append(Slider(ax, param_name, self.unique_params[i][0],
                                           self.unique_params[i][-1], valstep=self.unique_params[i]))
            self.sliders[-1].label.set_size(self.fontsize)
        # Tell the sliders to call the function self.update when a value changes
        for slider in self.sliders:
            slider.on_changed(self.update)

    def init_radio(self):
        """
        Makes the radio buttons. These buttons will trigger all available models of a given parameter to be showed
        (given all the other parameters)
        :return:
        """
        # Define the box in which the buttons will be displayed
        rax = plt.axes([0.05 + self.slide_cols * (self.length + self.h_space),
                        0.02,
                        0.125 * (9 / 16),
                        0.125])
        # Add a button that says None to only show the specified parameters
        # Assume last parameter is vsini which is calculated on the fly, so leave that out
        button_names = ["None"] + self.parameter_names
        self.radio_buttons = RadioButtons(rax, button_names)#, fontsize=self.fontsize)
        for label in self.radio_buttons.labels:
            label.set_size(self.fontsize)
        self.radio_buttons.on_clicked(self.update)  # Also call self.update when a button is pressed

    def init_plot(self, extra_wave=None, extra_flux=None, extra_error=None):
        """
        Initialize the figure
        :return:
        """
        # self.fig, self.axarr = plt.subplots(self.nrows, self.ncols, figsize=self.figsize)
        gs = self.fig.add_gridspec(4, 2)
        self.axarr = []
        for i in range(4):
            if i > 0:
                self.axarr.append(plt.subplot(gs[i,0], sharex=self.axarr[-1]))
            else:
                self.axarr.append(plt.subplot(gs[i,0]))

        self.axarr.append(plt.subplot(gs[:,1], aspect=1))
        # self.axarr = plt.add_subplot

        cmap = matplotlib.cm.get_cmap("viridis")
        colors = [cmap(val) for val in np.linspace(0, 1, self.max_models)]

        for i in range(len(self.line_names)):
            # Choose the relevant subplot
            # ax = self.axarr[i // self.ncols][i % self.ncols]
            ax = self.axarr[i]

            # Hard coded bit to fix plot ranges
            if i < 4:
                ax.set_xlim(0, np.pi * 2)
                # ax.set_ylim(-1, 1)
            elif i == 4:
                ax.set_xlim(-1, 1)
                ax.set_ylim(-1, 1)

            if i >= len(self.line_names):
                ax.remove()
                continue
            else:
                ax.set_title(self.line_names[i], fontsize=self.fontsize)
                # Create a list in which the lines are stored, these will be updated, rather than new lines plotted
                self.mpl_lines.append([])
                line, = ax.plot(self.line_profiles[0][i][0], self.line_profiles[0][i][1], c=colors[0])
                self.mpl_lines[-1].append(line)
                for j in range(1, self.max_models):
                    line, = ax.plot([], [], c=colors[j])
                    self.mpl_lines[-1].append(line)
                # ax.axhline(1, ls="--", c="0.5", alpha=0.5, zorder=-1)

                # specify the x limits if desired, otherwise it will be based on what
                if self.use_wave_range:
                    xmin, xmax = self.line_dict[self.line_names[i]][1:]
                    ax.set_xlim([xmin, xmax])

                if not isinstance(extra_wave, type(None)) and not isinstance(extra_flux, type(None)):
                    minw, maxw = ax.get_xlim()
                    sel = (extra_wave > minw) * (extra_wave < maxw)
                    if not isinstance(extra_error, type(None)):
                        ax.errorbar(extra_wave[sel], extra_flux[sel], yerr=extra_error[sel],
                                    fmt='o', color='0.5', ms=0, zorder=-1, alpha=0.5)
                    else:
                        ax.plot(extra_wave[sel], extra_flux[sel], c="0.5", zorder=-1, alpha=0.5)

        plt.tight_layout()
        plt.subplots_adjust(left=0.05, bottom=0.20, top=0.95, right=0.90)

        # Add the colorbar
        cbar_ax = self.fig.add_axes([0.91, 0.2, 0.025, 0.7])
        self.cb = self.fig.colorbar(self.colormap, cax=cbar_ax, orientation="vertical")
        self.cb.set_label("None", labelpad=-1, fontsize=self.fontsize)#, fontsize=self.fontsize)
        self.cb.ax.tick_params(labelsize=self.fontsize)

        # Initialize sliders and radio buttons
        self.init_sliders()
        self.init_radio()

        # gs.tight_layout(rect=[0.05, 0.20, 0.95, 0.90])

        plt.show()

    def add_line(self, line, wave, flux):#, line_name, vsini):
        """
        Updates the the x and y data of the specified matplotlib line object
        """
        # res, min_wave, max_wave = self.line_dict[line_name]
        # wave, flux = broaden_fwline(wave, flux, vsini, res)
        line.set_data(wave, flux)

    def update_colorbar(self):
        """
        Updates the colorbar
        :return:
        """
        if self.radio_buttons.value_selected == "None":
            self.norm = matplotlib.colors.Normalize(0, 1)
            self.colormap = matplotlib.cm.ScalarMappable(norm=self.norm)
        else:
            self.norm = matplotlib.colors.Normalize(self.param_dict[self.radio_buttons.value_selected][0],
                                               self.param_dict[self.radio_buttons.value_selected][-1])
            self.colormap = matplotlib.cm.ScalarMappable(self.norm)
        self.cb.update_normal(self.colormap)
        self.cb.set_label(self.radio_buttons.value_selected)

    def update(self, val):
        """
        Update the figure after the parameter selection has changed
        """
        # make an array of booleans and mark every matching models as True, assume everything matches at first
        selection = np.ones(self.model_parameters.shape[0], dtype=bool)
        for i, param_name in enumerate(self.parameter_names):
            if "sin i" not in param_name and param_name != self.radio_buttons.value_selected:
                selection *= self.sliders[i].val == self.model_parameters[:, i]
            else:
                vsini = self.sliders[i].val

        # Check the number of matching models
        selected_models = int(np.sum(selection))

        # If 1 model matches
        if selected_models == 1:
            model_lines = self.line_profiles[selection][0]

            for i, lines in enumerate(self.mpl_lines):

                wave, flux = model_lines[i]
                # if wave[-1] - wave[0] < 0.01:
                #     print("THIS LINE IS WEIRD! %s" % self.line_names[i])
                #     lines[0].set_data([], [])
                # else:
                self.add_line(lines[0], wave, flux)

        # If multiple models are selected with a radio button
        elif selected_models > 1:

            param_index = self.parameter_names.index(self.radio_buttons.value_selected)
            sel_order = np.argsort(self.model_parameters[selection, param_index])

            for i, model_lines in enumerate(self.line_profiles[selection][sel_order]):
                for j, lines in enumerate(self.mpl_lines):

                    wave, flux = model_lines[j]
                    # if wave[-1] - wave[0] < 0.01:
                    #     print("THIS LINE IS WEIRD! %s" % self.line_names[i])
                    #     lines[i].set_data([], [])
                    # else:
                    self.add_line(lines[i], wave, flux)

        # remove unused lines, if no models match all lines are removed
        for lines in self.mpl_lines:
            for j in range(selected_models, self.active_lines):
                lines[j].set_data([], [])

        # set the number of active lines to the current number
        self.active_lines = selected_models

        # Update the y axis range for each of the plots
        # for ax in np.ravel(self.axarr):
        #     ax.relim()
        #     ax.autoscale(axis="y")

        self.update_colorbar()
        self.fig.canvas.draw_idle()




