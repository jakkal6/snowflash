import numpy as np
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt


class SnowSlider:
    def __init__(self,
                 y_vars,
                 n_integrate,
                 model_sets,
                 x_factor=None,
                 y_factor=None,
                 ):
        """Handles a slider plot

        Parameters
        ----------
        y_vars : [str]
            List of y-variables being plotted
        n_integrate : [int]
            list of number of bins integrated over
        model_sets : [str]
        x_factor : float
        y_factor : float
        """
        self.y_vars = y_vars
        self.n_integrate = n_integrate
        self.model_sets = model_sets

        self.x_factor = check_factor(x_factor)
        self.y_factor = check_factor(y_factor)

        self.fig, self.ax, self.slider = self.setup()
        self.lines = None

    # =======================================================
    #                      Setup
    # =======================================================
    def setup(self, figsize=(8, 6)):
        """Setup slider fig

        Returns : fig, profile_ax, slider
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0.1, 0.2, 0.8, 0.65])
        slider_ax = fig.add_axes([0.1, 0.05, 0.8, 0.05])

        bin_min = self.n_integrate[0]
        bin_max = self.n_integrate[-1]

        slider = Slider(slider_ax, 'n_integrate', bin_min, bin_max, valinit=bin_max, valstep=1)

        return fig, ax, slider

    def get_ax_lines(self):
        """Return dict of labelled axis lines

        Note: assumes data plotted iteratively according to:
                    $ for all model_sets:
                    $    for all y_vars:
                    $        plot()
        """
        lines = {}
        n_yvars = len(self.y_vars)

        for i, model_set in enumerate(self.model_sets):
            lines[model_set] = {}

            for j, y_var in enumerate(self.y_vars):
                idx = i*n_yvars + j
                lines[model_set][y_var] = self.ax.lines[idx]

        self.lines = lines

    # =======================================================
    #                      Plot
    # =======================================================
    def update_ax_line(self, x, y, y_var, model_set):
        """Update x,y line values

        Parameters
        ----------
        x : array
        y : array
        y_var : str
        model_set : str
        """
        self.update_ax_x(x=x, y_var=y_var, model_set=model_set)
        self.update_ax_y(y=y, y_var=y_var, model_set=model_set)

    def update_ax_x(self, x, y_var, model_set):
        """Update x values

        Parameters
        ----------
        x : array
        y_var : str
        model_set : str
        """
        if self.lines is None:
            self.get_ax_lines()

        line = self.lines[model_set][y_var]
        line.set_ydata(x / self.y_factor)

    def update_ax_y(self, y, y_var, model_set):
        """Update y values

        Parameters
        ----------
        y : array
        y_var : str
        model_set : str
        """
        if self.lines is None:
            self.get_ax_lines()

        line = self.lines[model_set][y_var]
        line.set_ydata(y / self.y_factor)


# =======================================================
#                      Misc.
# =======================================================
def check_factor(factor):
    """Check provided axis scale factor
    """
    if factor is None:
        return 1
    else:
        return factor
