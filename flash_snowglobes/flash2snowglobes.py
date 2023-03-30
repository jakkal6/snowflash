# FLASH to snowglobes wrapper code
# Need working installation of snowglobes
# This will convert FLASH data to necessary input format for snowglobes,
# run snowglobes, extract the output, and clean up files

import sys
from astropy import units

# flash_snowglobes
from flash2snowglobes import flash_io, snow_cleanup, convert
from flash2snowglobes import write_files, analysis, run_snowglobes
from flash2snowglobes import snow_setup, flavor_mixing
from utils.config import Config
from utils import paths


if len(sys.argv) != 2:
    print('Must provide parameter(s):'
          + '\n1. config_name    # must match a file in flash_snowglobes/config/models/'
          )
    sys.exit(0)
else:
    config_name = sys.argv[1]


# ===== config and setup =====
config = Config(config_name)

distance = config.distance * units.kpc.to(units.cm)

t_bins = convert.get_bins(x0=config.bins['t_start'],
                          x1=config.bins['t_end'],
                          dx=config.bins['t_step'],
                          endpoint=False)

e_bins = convert.get_bins(x0=config.bins['e_start'],
                          x1=config.bins['e_end'],
                          dx=config.bins['e_step'],
                          endpoint=True)


print('=== Copying snowglobes install ===')
snow_setup.copy_snowglobes(config.paths['snowglobes'])


for mixing in config.mixing:
    for model_set in config.model_sets:
        for zams in config.zams_list:
            print('=== Converting flash data ===')
            dat_model_set = config.model_set_map.get(model_set, model_set)

            dat_filepath = paths.dat_filepath(models_path=config.paths['models'],
                                              model_set=dat_model_set,
                                              zams=zams,
                                              run=config.run)

            time, lum, avg, rms = flash_io.read_datfile(filepath=dat_filepath,
                                                        t_start=config.bins['t_start'],
                                                        t_end=config.bins['t_end'])

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
                               material=config.material,
                               detector=config.detector)

            print('=== Analyzing output ===')
            analysis.analyze_output(model_set=model_set,
                                    zams=zams,
                                    detector=config.detector,
                                    channel_groups=config.channel_groups,
                                    mixing=mixing)

            print('=== Cleaning up model ===')
            snow_cleanup.clean_model()

print('=== Final cleanup ===')
snow_cleanup.clean_all()
