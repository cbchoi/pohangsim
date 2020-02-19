import os
from config import TIME_STDDEV
exp1 = "python3 exp.py housewife bhs_N100_seed0  > blue_hs_"+str(TIME_STDDEV)+".log"
exp2 = "python3 exp.py housewife bsh_N100_seed0  > blue_sh_"+str(TIME_STDDEV)+".log"
exp3 = "python3 exp.py housewife sbh_N100_seed0  > stud_bh_"+str(TIME_STDDEV)+".log"
exp4 = "python3 exp.py housewife shb_N100_seed0  > stud_hb_"+str(TIME_STDDEV)+".log"
exp5 = "python3 exp.py housewife hsb_N100_seed0  > house_sb_"+str(TIME_STDDEV)+".log"
exp6 = "python3 exp.py housewife hbs_N100_seed0  > house_bs_"+str(TIME_STDDEV)+".log"
os.system(exp1)
os.system(exp2)
os.system(exp3)
os.system(exp4)
os.system(exp5)
os.system(exp6)
