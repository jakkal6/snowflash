import numpy as np
import xarray as xr

# snowflash
from snowflash.snow import snow_tools, snow_plot


class SnowModel:
    def __init__(self,
                 zams,
                 model_set,
                 detector,
                 mixing,
                 ):
        """Collection of SnowGlobes data

        parameters
        ----------
        zams : str
        model_set : str
        detector : str
        mixing : str
        """
        self.zams = zams
        self.model_set = model_set
        self.detector = detector
        self.mixing = mixing

        self.data = None
        self.counts = None
        self.rate = None
        self.cumulative = None
        self.e_sum = None
        self.t_sum = None
        self.e_avg = None

        self.load_counts()
        self.build_dataset()

    # ===============================================================
    #                      Load Tables
    # ===============================================================
    def load_counts(self):
        """Load time/energy binned count data
        """
        self.counts = snow_tools.load_counts(zams=self.zams,
                                             model_set=self.model_set,
                                             detector=self.detector,
                                             mixing=self.mixing)

    # ===============================================================
    #                      Analysis
    # ===============================================================
    def build_dataset(self):
        """Build Dataset of binned variables, and store 2D tables
        """
        counts = self.counts
        t_step = np.diff(counts['time'])[0]

        self.rate = counts / t_step
        self.cumulative = snow_tools.get_cumulative(counts)

        self.e_sum = counts.sum('energy').to_pandas()
        self.t_sum = counts.sum('time').to_pandas()

        self.e_avg = (counts['energy'] * counts).sum('energy') / self.e_sum
        self.e_avg = self.e_avg.to_pandas()

        self.data = xr.Dataset({'counts': self.counts,
                                'rate': self.rate,
                                'cumulative': self.cumulative,
                                'e_sum': self.e_sum,
                                't_sum': self.t_sum,
                                'e_avg': self.e_avg,
                                })

    # ===============================================================
    #                      Plotting
    # ===============================================================
    def plot_bin(self,
                 fixed_bin,
                 fixed_value,
                 cumulative=False,
                 channels=None,
                 ax=None,
                 title=True,
                 data_only=False,
                 ):
        """Plot energy bins for given time

        parameters
        ----------
        fixed_bin :str
        fixed_value :flt
        cumulative : bool
        channels : [str]
        ax : Axis
        title : bool
        data_only : bool
        """
        x_bin = {'energy': 'time', 'time': 'energy'}[fixed_bin]

        if cumulative:
            counts = self.cumulative
        else:
            counts = self.counts

        snow_plot.plot_bin(counts=counts,
                           x_bin=x_bin,
                           fixed_bin=fixed_bin,
                           fixed_value=fixed_value,
                           channels=channels,
                           ax=ax,
                           title=title,
                           data_only=data_only)

    def plot_sum(self,
                 x_bin,
                 sum_bin,
                 cumulative=False,
                 channels=None,
                 ax=None,
                 data_only=False,
                 ):
        """Plot energy bins for given time

        parameters
        ----------
        x_bin : str
        sum_bin : str
        cumulative : bool
        channels : [str]
        ax : Axis
        data_only : bool
        """
        if cumulative:
            counts = self.cumulative
        else:
            counts = self.counts

        snow_plot.plot_bin(counts=self.counts.sum(sum_bin),
                           x_bin=x_bin,
                           channels=channels,
                           ax=ax,
                           title=False,
                           data_only=data_only)
