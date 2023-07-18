# snowflash
from snowflash.utils import Config, paths, plot
from snowflash.flash import flash_fluences, flash_mixing, flash_io


def _check_bin_args(t_bin, e_bin):
    if ((t_bin is None) and (e_bin is None)) \
            or ((t_bin is not None) and (e_bin is not None)):
        raise ValueError('Must specify exactly one of t_bin or e_bin')

    bin_sel = None
    if isinstance(t_bin, int) or isinstance(e_bin, int):
        bin_sel = 'index'
    elif isinstance(t_bin, float) or isinstance(e_bin, float):
        bin_sel = 'value'

    return bin_sel


class FlashModel:
    """Object representing single FLASH simulation
    """

    def __init__(self,
                 zams,
                 model_set,
                 run,
                 config_name,
                 recalc=False,
                 ):
        """
        Parameters
        ----------
        zams : str, int or flt
        model_set : str
        run : str or None
        config_name : str
        recalc : bool
        """
        self.config = Config(config_name)
        self.zams = zams
        self.model_set = model_set
        self.run = run
        self.models_path = self.config.paths['models']
        self.recalc = recalc

        self.dat = None
        self.t_bins = None
        self.e_bins = None
        self.fluences = {}

        # run analysis
        self.get_bins()
        self.get_fluences()
        self.mix_fluences()

    # =======================================================
    #                 Loading data
    # =======================================================
    def get_fluences(self):
        """Calculate neutrino fluences from flash in time and energy bins
        """
        def recalc():
            self.read_datfile()
            self.calc_fluences()

        if self.recalc:
            recalc()
        else:
            try:
                self.load_fluences('raw')

            except (FileNotFoundError, ValueError) as err:
                if isinstance(err, FileNotFoundError):
                    print('No fluence file found. Reloading dat')
                else:
                    print('Fluence file incompatible with config. Reloading dat')
                recalc()

    def read_datfile(self):
        """Read time-dependent neutrino data from flash dat file
        """
        filepath = paths.flash_dat_filepath(models_path=self.models_path,
                                            zams=self.zams,
                                            model_set=self.model_set,
                                            run=self.run)

        self.dat = flash_io.read_datfile(filepath=filepath,
                                         t_start=self.config.bins['t_start'],
                                         t_end=self.config.bins['t_end'])

    def load_fluences(self, flu_type):
        """Load fluences from file

        Parameters
        ----------
        flu_type : 'raw' or 'mixed'
        """
        fluences = flash_io.load_fluences(zams=self.zams,
                                          model_set=self.model_set,
                                          flu_type=flu_type)

        if (len(self.t_bins) not in fluences.shape) \
                or (len(self.e_bins) not in fluences.shape):
            raise ValueError

        self.fluences[flu_type] = fluences

    # =======================================================
    #                 Saving data
    # =======================================================
    def save_fluences(self, flu_type):
        """Save fluences to file

        Parameters
        ----------
        flu_type : 'raw' or 'mixed'
        """
        flash_io.save_fluences(fluences=self.fluences[flu_type],
                               zams=self.zams,
                               model_set=self.model_set,
                               flu_type=flu_type)

    def write_snow_fluences(self, mixing):
        """Write fluence tables to file for snowglobes input

        Parameters
        ----------
        mixing : str
        """
        print('Writing fluences to file')
        flash_io.write_snow_fluences(model_set=self.model_set,
                                     zams=self.zams,
                                     t_bins=self.t_bins,
                                     e_bins=self.e_bins,
                                     fluences=self.fluences['mixed'].sel(mix=mixing))

    # =======================================================
    #                 Fluences
    # =======================================================
    def get_bins(self, decimals=5):
        """Generate time and energy bin coordinates

        Parameters
        ----------
        decimals : int
            number of decimals to round to
        """
        self.t_bins = flash_fluences.get_bins(x0=self.config.bins['t_start'],
                                              x1=self.config.bins['t_end'],
                                              dx=self.config.bins['t_step'],
                                              endpoint=False,
                                              decimals=decimals)

        self.e_bins = flash_fluences.get_bins(x0=self.config.bins['e_start'],
                                              x1=self.config.bins['e_end'],
                                              dx=self.config.bins['e_step'],
                                              endpoint=True,
                                              decimals=decimals)

    def calc_fluences(self):
        """Calculate neutrino fluences from flash in time and energy bins
        """
        self.fluences['raw'] = flash_fluences.calc_fluences(time=self.dat['time'],
                                                            lum=self.dat['lum'],
                                                            avg=self.dat['avg'],
                                                            rms=self.dat['rms'],
                                                            distance=self.config.distance,
                                                            t_bins=self.t_bins,
                                                            e_bins=self.e_bins)
        self.save_fluences('raw')

    def mix_fluences(self):
        """Apply flavor mixing to neutrino fluences
        """
        print('Applying flavor mixing to fluences')
        self.fluences['mixed'] = flash_mixing.mix_fluences(fluences=self.fluences['raw'],
                                                           mixing=self.config.mixing)
        self.save_fluences('mixed')

    # =======================================================
    #                 Plotting
    # =======================================================
    def plot_fluences_raw(self, t_bin=None, e_bin=None, ax=None, figsize=None):
        """Plot neutrino fluences versus time or energy bins

        Parameters
        ----------
        t_bin : int or flt
        e_bin : int or flt
        ax
        figsize
        """
        bin_sel = _check_bin_args(t_bin, e_bin)
        fig, ax = plot.setup_fig_ax(ax=ax, figsize=figsize)

        fluences = None
        if bin_sel == 'index':
            if t_bin is None:
                fluences = self.fluences['raw'].isel(energy=e_bin)
            else:
                fluences = self.fluences['raw'].isel(time=t_bin)
        elif bin_sel == 'value':
            if t_bin is None:
                fluences = self.fluences['raw'].sel(energy=e_bin)
            else:
                fluences = self.fluences['raw'].sel(time=t_bin)

        for flav in fluences.flav.values:
            ax.step(fluences.energy, fluences.sel(flav=flav), where='pre', label=flav)

        ax.legend()
