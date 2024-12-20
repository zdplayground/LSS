#!/bin/bash

set -e

source /global/common/software/desi/desi_environment.sh main
export LSSCODE=$HOME
PYTHONPATH=$PYTHONPATH:$LSSCODE/LSS/py

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld y --verspec iron --survey Y1 --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --basedir /global/cfs/cdirs/desi/survey/catalogs/ --verspec iron --type LRG --combwspec n --fullr y --survey Y1 --maxr 18 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --add_veto y --verspec iron --survey Y1 --maxr 0 --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/   --verspec iron --survey Y1 --fillran y --apply_veto y --add_veto y --maxr 18 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --verspec iron --survey Y1  --mkHPmaps y --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --apply_veto y --verspec iron --survey Y1 --maxr 0 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/   --verspec iron --survey Y1 --add_tl y --maxr 18 --par n --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --apply_map_veto y --verspec iron --survey Y1 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --verspec iron --add_weight_zfail y --survey Y1  --use_map_veto _HPmapcut --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG  --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --swap20211212 y --verspec iron --survey Y1 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --imsys y --survey Y1 --verspec iron --imsys_zbin y --use_map_veto _HPmapcut --version $1

python $LSSCODE/LSS/scripts/main/patch_HPmapcut.py --tracers LRG --survey Y1 --verspec iron --version $1

srun -N 1 -C cpu -t 04:00:00 --qos interactive --account desi python scripts/main/mkCat_main.py --type LRG --fulld n --survey Y1 --verspec iron --version $1 --clusd y --clusran y --splitGC y --nz y --par y --imsys_colname WEIGHT_IMLIN --basedir /global/cfs/cdirs/desi/survey/catalogs/

