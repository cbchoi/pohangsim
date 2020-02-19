import os, sys
from config import STDDEV
exp1 = "python3 exph.py housewife > housewife_"+str(STDDEV)+".log"
exp2 = "python3 expb.py bluecollar  > bluecollar_"+str(STDDEV)+".log"
exp3 = "python3 exps.py student > student_"+str(STDDEV)+".log"
os.system(exp1)
os.system(exp2)
os.system(exp3)
