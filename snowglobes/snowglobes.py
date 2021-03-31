import matplotlib.pyplot as plt

# snowglobes
from . import snow_tools
from . import snow_plot
from . import config


class SnowGlobesData:
    def __init__(self,
                 model_sets=('LMP', 'LMP+N50', 'SNA'),
                 tabs=(1, 2, 3),
                 detector='ar40kt',
                 load_data=True):
        """Collection of SnowGlobes data

        parameters
        ----------
        model_sets : [str]
            Labels for model sets
        tabs : [int]
            filename IDs that correspond to the model_sets
        detector : str
            Type of neutrino detector used in snowglobes
        load_data : bool
            immediately load all data
        """
        self.detector = detector
        self.model_sets = model_sets
        self.tabs = tabs

        self.channels = config.channels[detector]
        self.mass_list = config.mass_list
        self.n_mass = len(self.mass_list)

        self.summary_tables = None
        self.mass_tables = None
        self.prog_table = None

        if load_data:
            self.load_summary_tables()
            self.load_mass_tables()
            self.prog_table = snow_tools.load_prog_table()

    # ===============================================================
    #                      Load Tables
    # ===============================================================
    def load_summary_tables(self):
        """Load all time-integrated summary tables
        """
        print('Loading summary tables')
        tables = dict.fromkeys(self.model_sets)

        for i, tab in enumerate(self.tabs):
            model_set = self.model_sets[i]
            tables[model_set] = snow_tools.load_summary_table(tab=tab,
                                                              detector=self.detector)
        self.summary_tables = tables

    def load_mass_tables(self):
        """Load time-dependent tables for all individual mass models
        """
        tables = dict.fromkeys(self.model_sets)

        for i, tab in enumerate(self.tabs):
            model_set = self.model_sets[i]
            tables[model_set] = {}

            for j, mass in enumerate(self.mass_list):
                print(f'\rLoading mass tables, {model_set}: {j+1}/{self.n_mass}', end='')

                table = snow_tools.load_mass_table(mass=mass,
                                                   tab=tab,
                                                   detector=self.detector)
                tables[model_set][mass] = table

            print()

        self.mass_tables = tables

    # ===============================================================
    #                      Plotting
    # ===============================================================
    def plot_summary(self, column,
                     x_var='m_fe',
                     marker='.',
                     x_scale=None,
                     y_scale='linear',
                     legend=True,
                     figsize=None,
                     ax=None):
        """Plot quantity from summary table

        parameters
        ----------
        column : str
            which column to plot from summary_tables
        x_var : str
        marker : str
        y_scale : str
        x_scale : str
        legend : bool
        figsize : (width, length)
        ax : Axis
        """
        fig, ax = snow_plot.plot_summary(tables=self.summary_tables,
                                         column=column, x_var=x_var,
                                         prog_table=self.prog_table,
                                         x_scale=x_scale, y_scale=y_scale,
                                         marker=marker,
                                         figsize=figsize, legend=legend,
                                         ax=ax)
        return fig, ax

    def plot_time(self, column, mass,
                  x_scale='linear', y_scale='log', ax=None):
        """Plot time-dependent quantity from mass tables

        parameters
        ----------
        column : str
            which column to plot from mass_tables
        mass : float or int
        y_scale : str
        x_scale : str
        ax : Axis
        """
        fig, ax = snow_plot.plot_time(mass_tables=self.mass_tables,
                                      column=column, mass=mass,
                                      x_scale=x_scale, y_scale=y_scale,
                                      ax=ax)
        return fig, ax
