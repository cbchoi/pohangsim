import os, sys
import random

for i in range(1,31):
	random.seed(i)
	print(i)
	EXPORT204 = "python3 building_test.py > blue_3m_"+str(i)+".log"    #EXPORT 설정
	#xx= "python3 average_satisfaction.py"
	os.system(EXPORT204) 
	#os.system(xx)
