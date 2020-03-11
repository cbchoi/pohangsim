import sys   
file = open(sys.argv[1],'r')
lines = file.readlines()
file.close()

report_time=0
satisfaction=0
count_num=0

for i in range(len(lines)):
	line = lines[i].split('\n')[0]
	item =line.split(',')
	item.split(':')

	elif line=="reported":
		report_time+=1
	else:
		pass
		elements=line.split(":")
		satisfaction+=float(elements[1])
		count_num+=1
#avg=satisfaction/count_num
#print (avg)
print(report_time)
