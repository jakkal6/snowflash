# ===== Model setup =====
detector = "ar40kt"
mixing = ['nomix', 'normal', 'inverted']
model_sets = ['sn1987a']
run = 'run'

# names used in sim files (if different from model_set)
model_set_map = {}

# paths
snowglobes_path = "/mnt/research/SNAPhU/zac/snowglobes"
models_path = '/mnt/research/SNAPhU/sn1987a/runs'

# progenitor ZAMS masses [Msun]
masses = ('15-7b', '15-8b', '16-4a', '16-7b', '17-7a')

# source distance [kpc]
distance = 51.4

# time bins [s]
t_start = -0.05  # relative to bounce
t_end = 1.0
dt = 0.005

# energy bins [GeV]
e_start = 0.0
e_end = 0.1
e_step = 0.0002
