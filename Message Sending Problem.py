import random
import math

n = input('Enter the number of trials: ')
k = input('Enter the degree of message spreading: ')
s = input('Enter the number of Students: ')
intcount = 0
add = 0

for counter in range(1,n):

	#print '\n'

	a = []
	index = 0
	i = 1
	
	while i <= math.log(s)/math.log(k) + 1:
		j = 1
		
		while j <= k**intcount:
			randnum = random.randint(1,s)
			for item in a:
				if randnum == item:
					index = -1
			if index != -1:
				a.append(randnum)
				#print str(randnum) + ' appended in ', a
				
				
			else:
				#print str(randnum) + ' is repeated after ' + str(len(a)) + ' passes'
				add += len(a)
				break
			j += 1
		
		if index == -1:
			break

		intcount += 1
		i += 1

avg = float(add)/n
print "average for %d trials:" % n, avg
