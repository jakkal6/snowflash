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

        self.counts = None
        self.load_counts()

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

    # ===============================================================
    #                      Plotting
    # ===============================================================
    def plot_bin(self,
                 x_bin,
                 fixed_bin,
                 fixed_value,
                 channels=None,
                 ax=None,
                 title=True,
                 data_only=False,
                 ):
        """Plot energy bins for given time

        parameters
        ----------
        x_bin : flt
        fixed_bin :str
        fixed_value :flt
        channels : [str]
        ax : Axis
        title : bool
        data_only : bool
        """
        snow_plot.plot_bin(counts=self.counts,
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
                 channels=None,
                 ax=None,
                 data_only=False,
                 ):
        """Plot energy bins for given time

        parameters
        ----------
        x_bin : str
        sum_bin : str
        channels : [str]
        ax : Axis
        data_only : bool
        """
        snow_plot.plot_bin(counts=self.counts.sum(sum_bin),
                           x_bin=x_bin,
                           channels=channels,
                           ax=ax,
                           title=False,
                           data_only=data_only)
