import os, sys
stddev= sys.argv[1]
exp1 = "python3 exph.py housewife "+stddev+" > housewife_"+stddev+".log"
exp2 = "python3 expb.py bluecollar "+stddev+" > bluecollar_"+stddev+".log"
exp3 = "python3 exps.py student "+stddev+" > student_"+stddev+".log"
os.system(exp1)
os.system(exp2)
os.system(exp3)
