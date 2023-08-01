import numpy as np
import pandas as pd
import xarray as xr

# snowflash
from snowflash.snow import snow_tools, snow_plot
from snowflash.utils.config import Config


class SnowModel:
    def __init__(self,
                 zams,
                 model_set,
                 detector,
                 mixing,
                 recalc=True,
                 config=None,
                 ):
        """Collection of SnowGlobes data

        parameters
        ----------
        zams : str
        model_set : str
        detector : str
        mixing : str
        recalc : bool
        config : str
        """
        self.zams = zams
        self.model_set = model_set
        self.detector = detector
        self.mixing = mixing
        self.recalc = recalc
        self.config = Config({None: model_set}.get(config, config))

        self.data = None
        self.counts = None
        self.rate = None
        self.cumulative_t = None
        self.cumulative_e = None
        self.sum_e = None
        self.sum_t = None
        self.e_tot = None
        self.e_avg = None
        self.summary = None

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
            self.cumulative_t = self.counts.cumsum('time')
            self.cumulative_e = self.counts.cumsum('energy')
            self.e_tot = self.counts['energy'] * self.counts

            # 2D arrays
            self.sum_t = self.counts.sum('time').to_pandas()
            self.sum_e = self.counts.sum('energy').to_pandas()
            self.e_avg = (self.e_tot.sum('energy') / self.sum_e).to_pandas()

        else:
            # 3D arrays
            self.counts = self.data.counts
            print('Extracting derived variables')
            self.rate = self.data.rate
            self.cumulative_t = self.data.cumulative_t
            self.cumulative_e = self.data.cumulative_e
            self.e_tot = self.data.e_tot

            # 2D arrays
            self.sum_t = self.data.sum_t.to_pandas()
            self.sum_e = self.data.sum_e.to_pandas()
            self.e_avg = self.data.e_avg.to_pandas()

        self.t_bins = self.counts.time.to_numpy()
        self.e_bins = self.counts.energy.to_numpy()
        self.channels = self.counts.channel.to_numpy()

        self.get_summary()

    def get_summary(self):
        """Calculate summary stats
        """
        print('Calculating summary stats')
        counts = self.sum_e.sum()
        e_tot = (self.sum_e * self.e_avg).sum()

        self.summary = pd.DataFrame({'counts': counts,
                                     'e_avg': e_tot/counts,
                                     'e_tot': e_tot,
                                     'frac': counts/counts['all'],
                                     'e_frac': e_tot/e_tot['all'],
                                     })

    def extract_dataset(self):
        """Build Dataset of binned variables
        """
        self.get_vars()

        print('Constructing dataset')
        self.data = xr.Dataset({'counts': self.counts,
                                'rate': self.rate,
                                'cumulative_t': self.cumulative_t,
                                'cumulative_e': self.cumulative_e,
                                'sum_t': self.sum_t,
                                'sum_e': self.sum_e,
                                'e_tot': self.e_tot,
                                'e_avg': self.e_avg,
                                })

        snow_tools.save_model_data(self.data,
                                   detector=self.detector,
                                   model_set=self.model_set,
                                   zams=self.zams,
                                   mixing=self.mixing)

    # ===============================================================
    #                      Plotting
    # ===============================================================
    def plot_time(self,
                  e_bin=None,
                  ax=None,
                  title=True,
                  data_only=False,
                  ):
        """Plot bins for given time

        parameters
        ----------
        e_bin : int
        ax : Axis
        title : bool
        data_only : bool
        """
        self._plot_bins(data=self.counts,
                        x_var='time',
                        sel_idx=e_bin,
                        ax=ax,
                        title=title,
                        data_only=data_only)

    def plot_energy(self,
                    t_bin=None,
                    ax=None,
                    title=True,
                    data_only=False,
                    ):
        """Plot bins for given time

        parameters
        ----------
        t_bin : int
        ax : Axis
        title : bool
        data_only : bool
        """
        self._plot_bins(data=self.counts,
                        x_var='energy',
                        sel_idx=t_bin,
                        ax=ax,
                        title=title,
                        data_only=data_only)

    def _plot_bins(self,
                   data,
                   x_var,
                   sel_idx,
                   ax=None,
                   title=True,
                   data_only=False,
                   ):
        """Plot bins for given time

        parameters
        ----------
        data : xr.DataArray
        x_var : str
        sel_idx : int
        ax : Axis
        title : bool
        data_only : bool
        """
        sel_var = {'time': 'energy', 'energy': 'time'}[x_var]
        
        if sel_idx is None:
            counts = data.sum(sel_var)
        else:
            counts = data.isel({sel_var: sel_idx})

        snow_plot.plot_bin(counts=counts,
                           x_var=x_var,
                           ax=ax,
                           x_label=self.config.ax_label(x_var),
                           y_label=self.config.ax_label('counts'),
                           title=title,
                           data_only=data_only)
        