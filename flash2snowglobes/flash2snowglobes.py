# FLASH to snowglobes wrapper code
# Need working installation of snowglobes
# This will convert FLASH data to necessary input format for snowglobes,
# run snowglobes, extract the output, and clean up files

from astropy import units

import read_flash
import cleanup
import config
import convert
import write_files
import analysis
import run_snowglobes
import setup
import flavor_mixing
import detectors

try:
    x = config.snowglobes_path
except AttributeError:
    raise FileNotFoundError('config file not found. Copy one from `configs/` to `flash2snowglobes/config.py`')


print('=== Copying snowglobes install ===')
setup.copy_snowglobes(config.snowglobes_path)

material = detectors.materials[config.detector]
channel_groups = detectors.channel_groups[material]
distance = config.distance * units.kpc.to(units.cm)

timebins = convert.get_bins(x0=config.t_start,
                            x1=config.t_end,
                            dx=config.dt,
                            endpoint=False)

e_bins = convert.get_bins(x0=config.e_start,
                          x1=config.e_end,
                          dx=config.e_step,
                          endpoint=True)

for mixing in config.mixing:
    for model_set in config.model_sets:
        for mass in config.masses:
            print('=== Converting flash data ===')
            dat_model_set = config.model_set_map.get(model_set, model_set)

            filepath = read_flash.dat_filepath(model_set=dat_model_set,
                                               mass=mass,
                                               models_path=config.models_path)

            time, lum, avg, rms = read_flash.read_datfile(filepath=filepath,
                                                          t_start=config.t_start,
                                                          t_end=config.t_end)

            fluences = convert.get_fluences(time=time,
                                            lum=lum,
                                            avg=avg,
                                            rms=rms,
                                            distance=distance,
                                            timebins=timebins,
                                            e_bins=e_bins)

            fluences_mixed = flavor_mixing.mix_fluences(fluences=fluences,
                                                        mixing=mixing)

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
                               detector=config.detector)

            print('=== Analyzing output ===')
            analysis.analyze_output(model_set=model_set,
                                    mass=mass,
                                    detector=config.detector,
                                    channel_groups=channel_groups,
                                    mixing=mixing)

            print('=== Cleaning up model ===')
            cleanup.clean_model()

print('=== Final cleanup ===')
cleanup.clean_all()
