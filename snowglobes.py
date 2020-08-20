from . import snow_tools
from . import config


class SnowGlobesData:
    def __init__(self,
                 model_sets=('LMP', 'LMP+N50', 'SNA'),
                 alphas=(1, 2, 3),
                 detector='ar40kt'):
        """Collection of SnowGlobes data

        parameters
        ----------
        model_sets : [str]
            Labels for model sets
        alphas : [int]
            filename IDs that correspond to the model_sets
        detector : str
            Type of neutrino detector used in snowglobes
        """
        self.detector = detector
        self.model_sets = model_sets
        self.alphas = alphas
        self.summary_tables = None
        self.mass_list = config.mass_list

    # ===============================================================
    #                      Load Tables
    # ===============================================================
    def load_summary_tables(self):
        """Load time-integrated summary tables
        """
        tables = dict.fromkeys(self.model_sets)

        for i, alpha in enumerate(self.alphas):
            model_set = self.model_sets[i]
            tables[model_set] = snow_tools.load_summary_table(alpha=alpha,
                                                              detector=self.detector)
        self.summary_tables = tables

