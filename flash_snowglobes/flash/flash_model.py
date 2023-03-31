
# flash_snowglobes
from flash_snowglobes import utils
from flash_snowglobes.flash import flash_io


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
        """
        self.zams = zams
        self.model_set = model_set
        self.run = run

        self.config = utils.config.Config(config_name)
        self.models_path = self.config.paths['models']

        self.dat_filepath = utils.paths.dat_filepath(models_path=self.models_path,
                                                     zams=self.zams,
                                                     model_set=self.model_set,
                                                     run=self.run)

        self.dat = flash_io.read_datfile(filepath=self.dat_filepath,
                                         t_start=self.config.bins['t_start'],
                                         t_end=self.config.bins['t_end'])
