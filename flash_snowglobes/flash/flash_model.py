
# flash_snowglobes
from flash_snowglobes.utils import config, paths
from flash_snowglobes.flash.flash_io import read_datfile
from flash_snowglobes.flash.flash_fluences import get_fluences, get_bins
from flash_snowglobes.flash.flash_mixing import mix_fluences


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
        self.zams = zams
        self.model_set = model_set
        self.run = run

        self.config = config.Config(config_name)
        self.models_path = self.config.paths['models']

        self.dat_filepath = None
        self.dat = None
        self.t_bins = None
        self.e_bins = None
        self.fluences = None
        self.fluences_mixed = {}

        # run analysis
        self.read_datfile()
        self.get_bins()
        self.get_fluences()
        self.mix_fluences()

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

    def get_bins(self):
        """Generate time and energy bins
        """
        self.t_bins = get_bins(x0=self.config.bins['t_start'],
                               x1=self.config.bins['t_end'],
                               dx=self.config.bins['t_step'],
                               endpoint=False)

        self.e_bins = get_bins(x0=self.config.bins['e_start'],
                               x1=self.config.bins['e_end'],
                               dx=self.config.bins['e_step'],
                               endpoint=True)

    def get_fluences(self):
        """Calculate neutrino fluences for each flavor in all time and energy bins
        """
        self.fluences = get_fluences(time=self.dat['time'],
                                     lum=self.dat['lum'],
                                     avg=self.dat['avg'],
                                     rms=self.dat['rms'],
                                     distance=self.config.distance,
                                     t_bins=self.t_bins,
                                     e_bins=self.e_bins)

    def mix_fluences(self):
        """Apply flavor mixing to neutrino fluences
        """
        print('Applying flavor mixing to fluences')
        for mixing in self.config.mixing:
            self.fluences_mixed[mixing] = mix_fluences(fluences=self.fluences,
                                                       mixing=mixing)
