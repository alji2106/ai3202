# Alixandria Jimenez
# Assignment 5: MDP


#m for map
m = [[],[],[],[],[],[],[],[]]
#u for utility
u = [[],[],[],[],[],[],[],[]]
#stores next move
move = [[],[],[],[],[],[],[],[]]
#as given in class
gamma = 0.9
#easy to change but seems to have no effect
epsilon = .0001
i = 7

world = "World1MDP.txt"
with open(world) as file:
	for line in file:
		data = line.split()
		for num in data:
			u[i].append(0)
			move[i].append([[],[]])
			#Mountain
			if(int(num) is 1):
				m[i].append(-1)
			#Snake
			elif(int(num) is 3):
				m[i].append(-2)
			#Barn
			elif(int(num) is 4):
				m[i].append(1)
			#Empty Space, End, Wall stay the same value
			else:
				m[i].append(int(num))
		i -= 1
u[7][9] = 50


def maxMove(a, b, c, d):
	bestab = 0
	bestcd = 0
	if (a[0] >= b[0]):
		bestab = a
	else:
		bestab = b
	if (c[0] >= d[0]):
		bestcd = c
	else:
		bestcd = d
	if (bestab[0] >= bestcd[0]):
		return bestab
	else:
		return bestcd


def utilityIteration(x, y):
	global u

	currentU = u[y][x]
	if m[y][x] is 2 or m[y][x] is 50:
		return
	# Making sure we're not falling off the map.
	# Or in python's case going to the other side of it.

	if y-1 < 0:
		down = 0
	else:
		down = u[y-1][x]
	if y + 1 > 7:
		up = 0
	else:
		up = u[y+1][x]
	if x-1 <0:
		left = 0
	else:
		left = u[y][x-1]
	if x+1 > 9:
		right = 0
	else:
		right = u[y][x+1]

	goingDown  = (0.8*down) + (0.1*left) + (0.1*right)
	goingUp    = (0.8*up) + (0.1*left) + (0.1*right)
	goingLeft  = (0.8*left) + (0.1*up) + (0.1*down)
	goingRight = (0.8*right) + (0.1*up) + (0.1*down)

	d  = [goingDown, y-1, x]
	uu = [goingUp, y+1, x]
	l  = [goingLeft, y, x-1]
	r  = [goingRight, y, x+1]

	best = maxMove(d, uu, l, r)

	u[y][x] = m[y][x] + (gamma * best[0])
	move[y][x][0] = best[1] 
	move[y][x][1] = best[2]

	return abs(currentU - u[y][x])

delta = 10
while (delta >= (epsilon *((1-gamma)/gamma))):
	delta = 0
	for y in range(7, -1, -1):
		for x in range(9, -1, -1):
			newDelta = utilityIteration(x, y)
			if (newDelta > delta):
				delta = newDelta

x = 0
y = 0
ind = 0

while not (x is 9 and y is 7 or ind >25):
	print "Node:  x", x, " ,  y", y, "    Utility: ", u[y][x]
	newx = move[y][x][1]
	y = move[y][x][0] 
	x = newx
	ind +=1
	if(u[y][x] == 50):
		print "Node:  x", x, " ,  y", y, "    Utility: ", u[y][x]
		break