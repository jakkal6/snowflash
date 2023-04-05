# flash_snowglobes
from flash_snowglobes.utils import config, paths
from flash_snowglobes.flash import flash_fluences, flash_mixing, flash_io


class FlashModel:
    """Object representing single FLASH simulation
    """

    def __init__(self,
                 zams,
                 model_set,
                 run,
                 config_name,
                 ):
        """
        Parameters
        ----------
        zams : str, int or flt
        model_set : str
        run : str or None
        config_name : str
        """
        self.config = config.Config(config_name)
        self.zams = zams
        self.model_set = model_set
        self.run = run
        self.models_path = self.config.paths['models']
        self.dat = None

        self.t_bins = None
        self.e_bins = None
        self.fluences = {}

        # run analysis
        self.read_datfile()
        self.get_bins()
        self.get_fluences()
        self.mix_fluences()

    # =======================================================
    #                 Flash data
    # =======================================================
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

    # =======================================================
    #                 Fluence data
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

    def get_fluences(self):
        """Calculate neutrino fluences from flash in time and energy bins
        """
        try:
            self.load_fluences('raw')
        except FileNotFoundError:
            self.calc_fluences()

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

    def save_fluences(self, flu_type):
        """Save fluences to file

        Parameters
        ----------
        flu_type : 'raw' or 'mixed'
        """
        fluences = {'raw': self.fluences['raw'], 'mixed': self.fluences}[flu_type]

        flash_io.save_fluences(fluences=fluences,
                               zams=self.zams,
                               model_set=self.model_set,
                               flu_type=flu_type)

    def load_fluences(self, flu_type):
        """Load fluences from file

        Parameters
        ----------
        flu_type : 'raw' or 'mixed'
        """
        self.fluences[flu_type] = flash_io.load_fluences(zams=self.zams,
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
