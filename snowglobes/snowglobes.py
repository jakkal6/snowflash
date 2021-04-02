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
                 mass_list=None,
                 load_data=True,
                 output_dir='mass_tables_nomix',
                 n_bins=20,
                 ):
        """Collection of SnowGlobes data

        parameters
        ----------
        model_sets : [str]
            Labels for model sets
        tabs : [int]
            filename IDs that correspond to the model_sets
        detector : str
            Type of neutrino detector used in snowglobes
        mass_list : [float]
            progenitor ZAMS masses of models
        load_data : bool
            immediately load all data
        output_dir : str
            name of directory containing snowglobes data
        n_bins : int
            number of timebins to integrate over
        """
        self.detector = detector
        self.model_sets = model_sets
        self.tabs = tabs
        self.output_dir = output_dir
        self.n_bins = n_bins
        self.channels = config.channels[detector]
        self.mass_list = mass_list
        self.summary_tables = None
        self.mass_tables = None
        self.prog_table = None

        if self.mass_list is None:
            self.mass_list = config.mass_list

        self.n_mass = len(self.mass_list)

        if load_data:
            self.load_mass_tables()
            self.integrate_summary()
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
                                                   detector=self.detector,
                                                   output_dir=self.output_dir)
                tables[model_set][mass] = table

            print()

        self.mass_tables = tables

    def integrate_summary(self, n_bins=None):
        """Integrate models over timebins
        """
        if n_bins is None:
            n_bins = self.n_bins

        ref_table = self.mass_tables[self.model_sets[0]][self.mass_list[0]]
        t0 = ref_table.loc[0]['Time']
        t1 = ref_table.loc[n_bins]['Time']
        print(f'Integrating timebins from {t0:.2f} to {t1:.2f} s')

        tables = {}
        for model_set in self.model_sets:
            print(f'Integrating: {model_set}')
            mass_tables = self.mass_tables[model_set]
            tables[model_set] = snow_tools.time_integrate(mass_tables=mass_tables,
                                                          n_bins=n_bins,
                                                          channels=self.channels)
        print()
        self.summary_tables = tables

    # ===============================================================
    #                      Plotting
    # ===============================================================
    def plot_summary(self, column,
                     x_var='m_fe',
                     marker='.',
                     x_scale=None,
                     y_scale=None,
                     x_lims=None,
                     y_lims=None,
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
        x_lims : [low, high]
        y_lims : [low, high]
        legend : bool
        figsize : (width, length)
        ax : Axis
        """
        fig, ax = snow_plot.plot_summary(tables=self.summary_tables,
                                         column=column,
                                         x_var=x_var,
                                         prog_table=self.prog_table,
                                         x_scale=x_scale,
                                         y_scale=y_scale,
                                         x_lims=x_lims,
                                         y_lims=y_lims,
                                         marker=marker,
                                         figsize=figsize,
                                         legend=legend,
                                         ax=ax)
        return fig, ax

    def plot_all_channels(self, var,
                          channels=None,
                          x_var='m_fe',
                          marker='.',
                          x_scale=None,
                          y_scale=None,
                          x_lims=None,
                          y_lims=None,
                          legend=True,
                          figsize=None,
                          ax=None):
        """Plot summary variable for all channels

        parameters
        ----------
        var : 'Tot' or 'Avg'
        channels : [str]
        x_var : str
        marker : str
        y_scale : str
        x_scale : str
        x_lims : [low, high]
        y_lims : [low, high]
        legend : bool
        figsize : (width, length)
        ax : Axis
        """
        if channels is None:
            channels = self.channels

        fig, ax = snow_plot.plot_all_channels(tables=self.summary_tables,
                                              var=var,
                                              channels=channels,
                                              x_var=x_var,
                                              prog_table=self.prog_table,
                                              x_scale=x_scale,
                                              y_scale=y_scale,
                                              x_lims=x_lims,
                                              y_lims=y_lims,
                                              marker=marker,
                                              figsize=figsize,
                                              legend=legend,
                                              ax=ax)
        return fig, ax

    def plot_difference(self, column, ref_model_set,
                        x_var='m_fe',
                        marker='.',
                        x_scale=None,
                        y_scale=None,
                        x_lims=None,
                        y_lims=None,
                        legend=True,
                        figsize=None,
                        ax=None):
        """Plot differences relative to a given model_set

        parameters
        ----------
        column : str
            which column to plot from summary_tables
        ref_model_set : str
                which model_set to use as the baseline for comparison
        x_var : str
        marker : str
        y_scale : str
        x_scale : str
        x_lims : [low, high]
        y_lims : [low, high]
        legend : bool
        figsize : (width, length)
        ax : Axis
        """
        fig, ax = snow_plot.plot_difference(tables=self.summary_tables,
                                            column=column,
                                            ref_model_set=ref_model_set,
                                            x_var=x_var,
                                            prog_table=self.prog_table,
                                            x_scale=x_scale,
                                            y_scale=y_scale,
                                            x_lims=x_lims,
                                            y_lims=y_lims,
                                            marker=marker,
                                            figsize=figsize,
                                            legend=legend,
                                            ax=ax)
        return fig, ax

    def plot_time(self, column, mass,
                  x_scale=None,
                  y_scale=None,
                  ax=None):
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
                                      column=column,
                                      mass=mass,
                                      x_scale=x_scale,
                                      y_scale=y_scale,
                                      ax=ax)
        return fig, ax
