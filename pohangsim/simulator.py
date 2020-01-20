import os, sys
import numpy as np

for i in range(1,31):
	np.random.seed(i)
	print(i)
	EXPORT204 = "python3 building_test.py > result.log"    #EXPORT 설정
	xx= "python3 average_satisfaction.py"
	os.system(EXPORT204) 
	os.system(xx)