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

# source distance [kpc]
distance = 10

# time bins [s]
t_start = -0.05  # relative to bounce
t_end = 0.05
dt = 0.01

# energy bins [GeV]
e_start = 0.0
e_end = 0.1
e_step = 0.0002
