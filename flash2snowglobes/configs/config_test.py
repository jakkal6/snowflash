from astropy import units

import convert


# ===== Model setup =====
detector = "ar40kt"
mixing = ['nomix', ]
model_sets = ['LMP', ]

# labels used in sim files
model_set_map = {'LMP': 'tab1',
                 'LMP+N50': 'tab2',
                 'SNA': 'tab3'}

# paths
snowglobes_path = "/mnt/research/SNAPhU/zac/snowglobes"
models_path = f'/mnt/research/SNAPhU/swasik/run_ecrates'

# progenitor ZAMS masses [Msun]
masses = (9.0, )

# source distance
distance = 10 * units.kpc.to(units.cm)

# time bins [s]
t_start = -0.05  # relative to bounce
t_end = 0.05
dt = 0.01

timebins = convert.get_bins(x0=t_start,
                            x1=t_end,
                            dx=dt,
                            endpoint=False)

# energy bins [GeV]
e_start = 0.0
e_end = 0.1
e_step = 0.0002

e_bins = convert.get_bins(x0=e_start,
                          x1=e_end,
                          dx=e_step,
                          endpoint=True)


# ===== Detection channels =====
detector_materials = {
    'wc100kt30prct': 'water',
    'icecube': 'water',
    'ar40kt': 'argon',
}

# grouping of detection channels for given material
channel_groups = {
    'water':
        {'IBD': ['ibd'],
         'ES': ['nue_e'],
         'nue_O16': ['nue_O16'],
         'nuebar_O16': ['nuebar_O16'],
         'NC': ['nc_nue_O16', 'nc_nuebar_O16',
                'nc_numu_O16', 'nc_numubar_O16',
                'nc_nutau_O16', 'nc_nutaubar_O16']
         },

    'argon':
        {'ES': ['nue_e', 'nuebar_e',
                'numu_e', 'numubar_e',
                'nutau_e', 'nutaubar_e'],
         'nue_Ar40': ['nue_Ar40'],
         'nuebar_Ar40': ['nuebar_Ar40'],
         'NC': ['nc_nue_Ar40', 'nc_nuebar_Ar40',
                'nc_numu_Ar40', 'nc_numubar_Ar40',
                'nc_nutau_Ar40', 'nc_nutaubar_Ar40']
         },
}

material = detector_materials[detector]
channel_groups = channel_groups[material]

