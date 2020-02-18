import os, sys

exp1 = "python3 exph.py > h"+sys.argv[1]+".log"
exp2 = "python3 expb.py > b"+sys.argv[1]+".log"
exp3 = "python3 exps.py > s"+sys.argv[1]+".log"
os.system(exp1)
os.system(exp2)
os.system(exp3)
