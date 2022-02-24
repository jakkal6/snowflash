# FLASH to snowglobes wrapper code
# Need working installation of snowglobes
# This will convert FLASH data to necessary input format for snowglobes,
# run snowglobes, analyze the output, and clean up files

import os
import read_flash
from astropy import units

import cleanup
import config
import convert
import write_files
import analysis
import run_snowglobes
import setup
import mixing

model_sets = ['LMP', 'LMP+N50', 'SNA']
tab_map = {'LMP': 1, 'LMP+N50': 2, 'SNA': 3}  # model set model_set IDs

mix_ordering = 'none'
# mix_ordering = 'normal'
# mix_ordering = 'inverted'

detector = "ar40kt"

masses = config.masses
material = config.detector_materials[detector]
channel_groups = config.channel_groups[material]
distance = config.distance * units.kpc.to(units.cm)

print('=== Copying snowglobes install ===')
setup.copy_snowglobes(config.snowglobes_path)

for model_set in model_sets:
    tab = tab_map.get(model_set, model_set)
    models_path = f'/mnt/research/SNAPhU/swasik/run_ecrates/run_ecrates_tab{tab}'

    for mass in masses:
        print('=== Converting flash data ===')

        dat_filename = f'stir_ecrates_tab{tab}_s{mass}_alpha1.25.dat'
        dat_filepath = os.path.join(models_path, f'run_{mass}', dat_filename)
        print(f'Reading: {dat_filepath}')

        time, lum, avg, rms = read_flash.read_datfile(dat_filepath=dat_filepath,
                                                      t_start=config.t_start,
                                                      t_end=config.t_end)

        timebins = convert.get_bins(x0=config.t_start,
                                    x1=config.t_end,
                                    dx=config.dt,
                                    endpoint=False)

        e_bins = convert.get_bins(x0=config.e_start,
                                  x1=config.e_end,
                                  dx=config.e_step,
                                  endpoint=True)

        fluences = convert.get_fluences(time=time,
                                        lum=lum,
                                        avg=avg,
                                        rms=rms,
                                        distance=distance,
                                        timebins=timebins,
                                        e_bins=e_bins)

        # Apply MSW neutrino mixing
        fluences_mixed = mixing.mix_fluences(fluences=fluences,
                                             ordering=mix_ordering)

        print('=== Writing input files ===')
        write_files.write_fluence_files(model_set=model_set,
                                        mass=mass,
                                        timebins=timebins,
                                        e_bins=e_bins,
                                        fluences_mixed=fluences_mixed)

        print('=== Running snowglobes ===')
        run_snowglobes.run(model_set=model_set,
                           mass=mass,
                           timebins=timebins,
                           material=material,
                           detector=detector)

        print('=== Analysing output ===')
        analysis.analyze_output(model_set=model_set,
                                mass=mass,
                                detector=detector,
                                channel_groups=channel_groups,
                                output=config.output)

        print('=== Cleaning up model ===')
        cleanup.mass()

print('=== Final cleanup ===')
cleanup.final()
