#!/bin/bash

set -e

source /global/common/software/desi/desi_environment.sh main
export LSSCODE=$HOME
PYTHONPATH=$PYTHONPATH:$LSSCODE/LSS/py

verspec=kibo-v1
survey=DA2

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld y --verspec $verspec --survey $survey --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type QSO --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld y --verspec $verspec --survey $survey --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main.py --type ELG_LOP --notqso y --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld y --verspec $verspec --survey $survey --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --basedir /global/cfs/cdirs/desi/survey/catalogs/ --verspec $verspec --type LRG --combwspec n --fullr y --survey $survey --maxr 18 --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --basedir /global/cfs/cdirs/desi/survey/catalogs/ --verspec $verspec --type QSO --combwspec n --fullr y --survey $survey --maxr 18 --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --basedir /global/cfs/cdirs/desi/survey/catalogs/ --verspec $verspec --type ELG_LOP --notqso y --combwspec n --fullr y --survey $survey --maxr 18 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --add_veto y --verspec $verspec --survey $survey --maxr 0 --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/   --verspec $verspec --survey $survey --fillran y --apply_veto y --add_veto y --maxr 18 --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --type QSO --basedir /global/cfs/cdirs/desi/survey/catalogs/   --verspec $verspec --survey $survey --fillran y --apply_veto y --maxr 18 --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --type ELG_LOP --notqso y --basedir /global/cfs/cdirs/desi/survey/catalogs/   --verspec $verspec --survey $survey --fillran y --apply_veto y --maxr 18 --version $1


python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --verspec $verspec --survey $survey  --mkHPmaps y --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type QSO --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --verspec $verspec --survey $survey  --mkHPmaps y --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type ELG_LOP --notqso y --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --verspec $verspec --survey $survey  --mkHPmaps y --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --apply_veto y --verspec $verspec --survey $survey --maxr 0 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type QSO --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --apply_veto y --verspec $verspec --survey $survey --maxr 0 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type ELG_LOP --notqso y --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --apply_veto y --verspec $verspec --survey $survey --maxr 0 --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/   --verspec $verspec --survey $survey --add_tl y --maxr 18 --par n --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --type QSO --basedir /global/cfs/cdirs/desi/survey/catalogs/   --verspec $verspec --survey $survey --add_tl y --maxr 18 --par n --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main_ran.py --type ELG_LOP --notqso y --basedir /global/cfs/cdirs/desi/survey/catalogs/   --verspec $verspec --survey $survey --add_tl y --maxr 18 --par n --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --apply_map_veto y --verspec $verspec --survey $survey --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main.py --type QSO --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --apply_map_veto y --verspec $verspec --survey $survey --version $1

srun -N 1 -C cpu -t 04:00:00 -q interactive python $LSSCODE/LSS/scripts/main/mkCat_main.py --type ELG_LOP --notqso y --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --apply_map_veto y --verspec $verspec --survey $survey --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --verspec $verspec --add_weight_zfail y --survey $survey  --use_map_veto _HPmapcut --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type QSO --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --verspec $verspec --add_weight_zfail y --survey $survey  --use_map_veto _HPmapcut --version $1

python $LSSCODE/LSS/scripts/main/mkCat_main.py --type ELG_LOP --notqso y --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --verspec $verspec --add_weight_zfail y --survey $survey  --use_map_veto _HPmapcut --version $1


python $LSSCODE/LSS/scripts/main/mkCat_main.py --type LRG --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n --imsys y --survey $survey --verspec $verspec --imsys_zbin y --use_map_veto _HPmapcut --version $1

python $LSSCODE/LSS/scripts/main/patch_HPmapcut.py --tracers LRG --survey Y1 --verspec $verspec --version $1

srun -N 1 -C cpu -t 04:00:00 --qos interactive --account desi python scripts/main/mkCat_main.py --type LRG --fulld n --survey $survey --verspec $verspec --version $1 --clusd y --clusran y --splitGC y --nz y --par y --imsys_colname WEIGHT_IMLIN --basedir /global/cfs/cdirs/desi/survey/catalogs/

srun -N 1 -C cpu -t 04:00:00 --qos interactive --account desi scripts/Y3_sysnetELG_zbins.sh $1

srun -N 1 -C cpu -t 04:00:00 --qos interactive --account desi python scripts/main/mkCat_main.py --type ELG_LOP --notqso y  --fulld n --survey $survey --verspec $verspec --version $1 --clusd y --clusran y --splitGC y --nz y --par y --imsys_colname WEIGHT_SN --basedir /global/cfs/cdirs/desi/survey/catalogs/

source /global/common/software/desi/users/adematti/cosmodesi_environment.sh main
export LSSCODE=$HOME
PYTHONPATH=$PYTHONPATH:$LSSCODE/LSS/py

python scripts/main/mkCat_main.py --type QSO--version $1  --basedir /global/cfs/cdirs/desi/survey/catalogs/  --fulld n  --regressis y --add_regressis y --survey $survey --verspec $verspec --imsys_zbin y

srun -N 1 -C cpu -t 04:00:00 --qos interactive --account desi python scripts/main/mkCat_main.py --type QSO  --fulld n --survey $survey --verspec $verspec --version $1 --clusd y --clusran y --splitGC y --nz y --par y --imsys_colname WEIGHT_RF --basedir /global/cfs/cdirs/desi/survey/catalogs/


mkdir /global/cfs/cdirs/desi/survey/catalogs/$survey/LSS/$verspec/LSScats/$1/nonKP/
mv /global/cfs/cdirs/desi/survey/catalogs/$survey/LSS/$verspec/LSScats/$1/*clustering* /global/cfs/cdirs/desi/survey/catalogs/$survey/LSS/$verspec/LSScats/$1/nonKP/