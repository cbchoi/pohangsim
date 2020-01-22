from statistics import mean
import matplotlib.pyplot as plt


file = open('onlyblue1.log','r')
lines = file.readlines()
file.close()

report_time=0
satisfaction=[]
plottime=[]
time = 0
for i in range(len(lines)):
	line = lines[i].split('\n')[0]
	if line.startswith("global"):
		break
	elif line=="reported":
		report_time+=1
	elif line.startswith("-----"):
		time +=1
	else:
		elements=line.split(":")
		satisfaction.append(int(elements[1]))
		plottime.append(time)

plt.hist(satisfaction,bins=10)
plt.show()
print (mean(satisfaction),report_time)