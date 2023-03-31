
# flash_snowglobes
from flash_snowglobes import utils
from flash_snowglobes.flash import flash_io, flash_fluences


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

        self.config = utils.config.Config(config_name)
        self.models_path = self.config.paths['models']

        self.t_bins = flash_fluences.get_bins(x0=self.config.bins['t_start'],
                                              x1=self.config.bins['t_end'],
                                              dx=self.config.bins['t_step'],
                                              endpoint=False)

        self.e_bins = flash_fluences.get_bins(x0=self.config.bins['e_start'],
                                              x1=self.config.bins['e_end'],
                                              dx=self.config.bins['e_step'],
                                              endpoint=True)

        self.dat_filepath = utils.paths.dat_filepath(models_path=self.models_path,
                                                     zams=self.zams,
                                                     model_set=self.model_set,
                                                     run=self.run)

        self.dat = flash_io.read_datfile(filepath=self.dat_filepath,
                                         t_start=self.config.bins['t_start'],
                                         t_end=self.config.bins['t_end'])

        self.fluences = flash_fluences.get_fluences(time=self.dat['time'],
                                                    lum=self.dat['lum'],
                                                    avg=self.dat['avg'],
                                                    rms=self.dat['rms'],
                                                    distance=self.config.distance,
                                                    t_bins=self.t_bins,
                                                    e_bins=self.e_bins)
