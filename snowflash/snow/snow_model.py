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
                 recalc=False,
                 ):
        """Collection of SnowGlobes data

        parameters
        ----------
        zams : str
        model_set : str
        detector : str
        mixing : str
        recalc : bool
        """
        self.zams = zams
        self.model_set = model_set
        self.detector = detector
        self.mixing = mixing
        self.recalc = recalc

        self.data = None
        self.counts = None
        self.rate = None
        self.cumulative = None
        self.e_sum = None
        self.t_sum = None
        self.e_tot = None
        self.e_avg = None
        self.totals = None

        self.t_bins = None
        self.e_bins = None
        self.channels = None

        self.get_data()

    # ===============================================================
    #                      Loading
    # ===============================================================
    def get_data(self):
        """Load dataset from file or re-extract
        """
        if self.recalc:
            self.extract_dataset()
        else:
            try:
                self.load_data()
            except FileNotFoundError:
                print('Dataset file not found; re-extracting')
                self.extract_dataset()

    def load_data(self):
        """Load complete dataset
        """
        self.data = snow_tools.load_model_data(zams=self.zams,
                                               model_set=self.model_set,
                                               detector=self.detector,
                                               mixing=self.mixing)
        self.get_vars()

    def get_vars(self):
        """Set binned variables, either re-calculated or pulled from file
        """
        if self.data is None:
            # 3D arrays
            self.counts = snow_tools.load_counts(zams=self.zams,
                                                 model_set=self.model_set,
                                                 detector=self.detector,
                                                 mixing=self.mixing)

            print('Calculating derived variables')
            self.rate = self.counts / np.diff(self.counts['time'])[0]
            self.cumulative = snow_tools.get_cumulative(self.counts)
            self.e_tot = self.counts['energy'] * self.counts

            # 2D arrays
            self.t_sum = self.counts.sum('time').to_pandas()
            self.e_sum = self.counts.sum('energy').to_pandas()
            self.e_avg = (self.e_tot.sum('energy') / self.e_sum).to_pandas()

        else:
            print('Extracting derived variables')
            # 3D arrays
            self.counts = self.data.counts
            self.rate = self.data.rate
            self.cumulative = self.data.cumulative
            self.e_tot = self.data.e_tot

            # 2D arrays
            self.t_sum = self.data.t_sum.to_pandas()
            self.e_sum = self.data.e_sum.to_pandas()
            self.e_avg = self.data.e_avg.to_pandas()

        self.t_bins = self.counts.time.to_numpy()
        self.e_bins = self.counts.energy.to_numpy()
        self.channels = self.counts.channel.to_numpy()

    def extract_dataset(self):
        """Build Dataset of binned variables
        """
        self.get_vars()

        print('Constructing dataset')
        self.data = xr.Dataset({'counts': self.counts,
                                'rate': self.rate,
                                'cumulative': self.cumulative,
                                't_sum': self.t_sum,
                                'e_sum': self.e_sum,
                                'e_tot': self.e_tot,
                                'e_avg': self.e_avg,
                                })

        snow_tools.save_model_data(self.data,
                                   detector=self.detector,
                                   model_set=self.model_set,
                                   zams=self.zams,
                                   mixing=self.mixing)

    def get_totals(self):
        """Calculate summary stats
        """
        self.totals = {'counts': {}}
        tot = self.counts.sum(['energy', 'time'])

        for i, channel in enumerate(self.channels):
            self.totals['counts'][channel] = tot.values[i]

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
