# FLASH to snowglobes wrapper code
# Need working installation of snowglobes
# This will convert FLASH data to necessary input format for snowglobes,
# run snowglobes, extract the output, and clean up files

import sys
from astropy import units

import flash_io
import snow_cleanup
import convert
import write_files
import analysis
import run_snowglobes
import snow_setup
import flavor_mixing


if len(sys.argv) != 2:
    print('Must provide parameter(s):'
          + '\n1. config_name    # must match a file in flash_snowglobes/config/models/'
          )
    sys.exit(0)
else:
    config_name = sys.argv[1]


# ===== config and setup =====
config = flash_io.load_config(config_name)
detector_config = flash_io.load_config('detectors')

snowglobes_path = config['paths']['snowglobes']
models_path = config['paths']['models']

run = config['models']['run']
model_sets = config['models']['model_sets']
model_set_map = config['models']['model_set_map']
zams_list = config['models']['zams']

t_start = config['bins']['t_start']
t_end = config['bins']['t_end']
t_step = config['bins']['t_step']

e_start = config['bins']['e_start']
e_end = config['bins']['e_end']
e_step = config['bins']['e_step']

detector = config['snow']['detector']
material = detector_config['materials'][detector]
channel_groups = detector_config['channel_groups'][material]

distance = config['snow']['distance'] * units.kpc.to(units.cm)

t_bins = convert.get_bins(x0=t_start, x1=t_end, dx=t_step, endpoint=False)
e_bins = convert.get_bins(x0=e_start, x1=e_end, dx=e_step, endpoint=True)


print('=== Copying snowglobes install ===')
snow_setup.copy_snowglobes(snowglobes_path)


for mixing in config['snow']['mixing']:
    for model_set in model_sets:
        for zams in zams_list:
            print('=== Converting flash data ===')
            dat_model_set = model_set_map.get(model_set, model_set)

            filepath = flash_io.dat_filepath(model_set=dat_model_set,
                                             zams=zams,
                                             models_path=models_path,
                                             run=run)

            time, lum, avg, rms = flash_io.read_datfile(filepath=filepath,
                                                        t_start=t_start,
                                                        t_end=t_end)

            fluences = convert.get_fluences(time=time,
                                            lum=lum,
                                            avg=avg,
                                            rms=rms,
                                            distance=distance,
                                            t_bins=t_bins,
                                            e_bins=e_bins)

            fluences_mixed = flavor_mixing.mix_fluences(fluences=fluences,
                                                        mixing=mixing)

            write_files.write_fluence_files(model_set=model_set,
                                            zams=zams,
                                            t_bins=t_bins,
                                            e_bins=e_bins,
                                            fluences_mixed=fluences_mixed)

            print('=== Running snowglobes ===')
            run_snowglobes.run(model_set=model_set,
                               zams=zams,
                               t_bins=t_bins,
                               material=material,
                               detector=detector)

            print('=== Analyzing output ===')
            analysis.analyze_output(model_set=model_set,
                                    zams=zams,
                                    detector=detector,
                                    channel_groups=channel_groups,
                                    mixing=mixing)

            print('=== Cleaning up model ===')
            snow_cleanup.clean_model()

print('=== Final cleanup ===')
snow_cleanup.clean_all()
