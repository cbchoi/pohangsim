file = open('result.log','r')
lines = file.readlines()
file.close()

report_time=0
satisfaction=0
count_num=0

for i in range(len(lines)):
	line = lines[i].split('\n')[0]
	if line=="global: 8760  del agent: clock":
		break
	elif line=="reported":
		report_time+=1
	else:
		elements=line.split(":")
		satisfaction+=int(elements[1])
		count_num+=1
avg=satisfaction/count_num
print (avg,report_time)

