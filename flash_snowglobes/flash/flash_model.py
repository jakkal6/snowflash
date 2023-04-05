# flash_snowglobes
from flash_snowglobes.utils import config, paths
from flash_snowglobes.flash import flash_fluences, flash_mixing
from flash_snowglobes.flash.flash_io import read_datfile, write_fluence_files


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
        self.dat_filepath = None
        self.dat = None

        self.t_bins = None
        self.e_bins = None
        self.fluences_raw = None
        self.fluences = None

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
        self.dat_filepath = paths.dat_filepath(models_path=self.models_path,
                                               zams=self.zams,
                                               model_set=self.model_set,
                                               run=self.run)

        self.dat = read_datfile(filepath=self.dat_filepath,
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
        """Calculate neutrino fluences for each flavor in all time and energy bins
        """
        fluences = flash_fluences.get_fluences(time=self.dat['time'],
                                               lum=self.dat['lum'],
                                               avg=self.dat['avg'],
                                               rms=self.dat['rms'],
                                               distance=self.config.distance,
                                               t_bins=self.t_bins,
                                               e_bins=self.e_bins)

        self.fluences_raw = flash_fluences.fluences_to_xarray(fluences=fluences,
                                                              t_bins=self.t_bins,
                                                              e_bins=self.e_bins)

    def mix_fluences(self):
        """Apply flavor mixing to neutrino fluences
        """
        print('Applying flavor mixing to fluences')
        self.fluences = flash_mixing.mix_fluences(fluences=self.fluences_raw,
                                                  mixing=self.config.mixing)

    def write_fluences(self, mixing):
        """Write fluence tables to file for snowglobes input

        Parameters
        ----------
        mixing : str
        """
        print('Writing fluences to file')
        write_fluence_files(model_set=self.model_set,
                            zams=self.zams,
                            t_bins=self.t_bins,
                            e_bins=self.e_bins,
                            fluences=self.fluences.sel(mix=mixing))
