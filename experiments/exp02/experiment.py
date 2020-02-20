import os
from config import *

import time
from functools import wraps

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.perf_counter()
        result = fn(*args, **kwargs)
        t2 = time.perf_counter()
        print("@timefn: {} took {} seconds".format(fn.__name__, t2 - t1))
        return result
    return measure_time

@timefn
def execute_fn(executable):
	os.system(ex)

#532
exp1 = "python3 exp.py bhs532_N100_seed0  > 532blue_hs_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp2 = "python3 exp.py bsh532_N100_seed0  > 532blue_sh_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp3 = "python3 exp.py sbh532_N100_seed0  > 532stud_bh_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp4 = "python3 exp.py shb532_N100_seed0  > 532stud_hb_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp5 = "python3 exp.py hsb532_N100_seed0  > 532house_sb_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp6 = "python3 exp.py hbs532_N100_seed0  > 532house_bs_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
#442
exp7 = "python3 exp.py hbs442_N100_seed0  > 442house_bs_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp8 = "python3 exp.py shb442_N100_seed0  > 442stud_hb_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp9 = "python3 exp.py sbh442_N100_seed0  > 442stud_bh_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
#721
exp10 = "python3 exp.py bhs721_N100_seed0  > 721blue_hs_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp11 = "python3 exp.py bsh721_N100_seed0  > 721blue_sh_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp12 = "python3 exp.py sbh721_N100_seed0  > 721stud_bh_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp13 = "python3 exp.py shb721_N100_seed0  > 721stud_hb_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp14 = "python3 exp.py hsb721_N100_seed0  > 721house_sb_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"
exp15 = "python3 exp.py hbs721_N100_seed0  > 721house_bs_"+str(TIME_STDDEV)+"trash"+str(TRASH_STDDEV)+"_"+str(GARBAGECAN_SIZE)+"_"+str(RANDOM_SEED)+".log"

ex_list = [exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8, exp9, exp10, exp11, exp12, exp13, exp14, exp15] 

total = len(ex_list)
for idx, ex in enumerate(ex_list):
	print(f"Processing {idx+1}/{total}:", ex)
	execute_fn(ex)

