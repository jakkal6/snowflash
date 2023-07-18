# FLASH to snowglobes wrapper code
# Need working installation of snowglobes
# This will convert FLASH data to necessary input format for snowglobes,
# run snowglobes, extract the output, and clean up files

import sys

# snowflash
from snowflash import FlashModel, Config
from snowflash.flash2snowglobes import analysis, snow_run, snow_cleanup

reload = False

if len(sys.argv) not in (2, 3):
    print('Must provide parameter(s):'
          + '\n1. config_name    # must match a file in snowflash/config/models/'
          + '\n(2. reload)'
          )
    sys.exit(0)
else:
    config_name = sys.argv[1]
    if len(sys.argv) == 3:
        reload = (sys.argv[2].lower() == 'true')


# ===== config and setup =====
config = Config(config_name)

print('=== Setting up snowglobes ===')
snow_run.setup_snowglobes(config.paths['snowglobes'])


for mixing in config.mixing:
    for model_set in config.model_sets:
        for zams in config.zams_list:
            print('=== Converting flash data ===')
            flash_model = FlashModel(zams=zams,
                                     model_set=model_set,
                                     run=config.run,
                                     config_name=config_name,
                                     reload=reload)

            flash_model.write_snow_fluences(mixing)

            print('=== Running snowglobes ===')
            snow_run.run(model_set=model_set,
                         zams=zams,
                         n_bins=len(flash_model.t_bins),
                         material=config.material,
                         detector=config.detector)

            print('=== Extracting output ===')
            analysis.extract_counts(model_set=model_set,
                                    zams=zams,
                                    detector=config.detector,
                                    channel_groups=config.channel_groups,
                                    mixing=mixing)

            analysis.analyze_output(model_set=model_set,
                                    zams=zams,
                                    detector=config.detector,
                                    channel_groups=config.channel_groups,
                                    mixing=mixing)

            print('=== Cleaning up files ===')
            snow_cleanup.clean_model()
