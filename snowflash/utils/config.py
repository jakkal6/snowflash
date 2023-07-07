"""Config class
"""
from configparser import ConfigParser
import ast
from astropy import units

# snowflash
from snowflash.utils import paths

kpc_to_cm = units.kpc.to(units.cm)


class ConfigError(Exception):
    pass


class Config:
    def __init__(self, name):
        """Holds and returns config values

        Parameters
        ----------
        name : str
            name of model config to load, e.g. 'sn1987a'
        """
        self.name = name
        self.configs = {'models': load_config(name),
                        'detectors': load_config('detectors'),
                        'plot': load_config('plotting')
                        }

        self.paths = self.get_section('models', 'paths')

        self.model_sets = self.get_param('models', 'flash', 'model_sets')
        self.run = self.get_param('models', 'flash', 'run')
        self.model_set_map = self.get_param('models', 'flash', 'model_set_map')
        self.zams_list = self.get_param('models', 'flash', 'zams_list')

        self.bins = self.get_section('models', 'bins')
        self.mixing = self.get_param('models', 'snow', 'mixing')
        self.distance = self.get_param('models', 'snow', 'distance') * kpc_to_cm

        self.detector = self.get_param('models', 'snow', 'detector')
        self.material = self.get_param('detectors', 'materials', self.detector)
        self.channel_groups = self.get_param('detectors', 'channel_groups', self.material)
        self.channels = list(self.channel_groups.keys())

    # ===============================================================
    #                  general config
    # ===============================================================
    def get_param(self, config_group, section, param):
        """Get config.section parameter

        Returns: str

        parameters
        ----------
        config_group : str
        section : str
        param : str
        """
        conf = self.get_section(config_group, section)

        if param not in conf:
            raise ConfigError(f"'{param}' not a valid {config_group}.{section} param")

        return conf[param]

    def get_section(self, config_group, section):
        """Get config section

        Returns: str

        parameters
        ----------
        config_group : str
        section : str
        """
        conf = self.configs[config_group]

        if section not in conf:
            raise ConfigError(f"'{section}' not a valid {config_group} config section")

        return conf[section]

    # ===============================================================
    #                  flash parameters
    # ===============================================================
    def flash(self, var):
        """Get axis scale for given section, default to 'linear'

        Returns : str

        parameters
        ----------
        var : str
        """
    # ===============================================================
    #                  plot parameters
    # ===============================================================
    def color(self, model_set):
        """Get color for given model_set

        Returns : str

        parameters
        ----------
        model_set : str
        """
        return self.get_param('plot', 'plot', 'colors').get(model_set)

    def ax_scale(self, var):
        """Get axis scale for given section, default to 'linear'

        Returns : str

        parameters
        ----------
        var : str
        """
        return self.get_param('plot', 'plot', 'ax_scales').get(var, 'linear')

    def ax_lims(self, var):
        """Get axis limits for given section

        Returns : [min, max]

        parameters
        ----------
        var : str
        """
        return self.get_param('plot', 'plot', 'ax_lims').get(var)

    def ax_label(self, var):
        """Get axis label for given section

        Returns : str

        parameters
        ----------
        var : str
        """
        return self.get_param('plot', 'plot', 'ax_labels').get(var, var)


def load_config(name):
    """Load .ini config file and return as dict

    Returns : {}

    parameters
    ----------
    name : str
    """
    filepath = paths.config_filepath(name)
    ini = ConfigParser()
    ini.read(filepath)
    config = {}

    for section in ini.sections():
        config[section] = {}

        for option in ini.options(section):
            config[section][option] = ast.literal_eval(ini.get(section, option))

    return config
