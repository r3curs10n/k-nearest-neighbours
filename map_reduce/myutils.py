import sys,math,random

K = 1000			# K nearest neighbours
C = 3			# no. of class labes. Can be at most 6 because we have only 6 colours :P
N = 10000		# total no. of points
jobSize = 1000	# no. of points given to each client
lowerBnd = 0	# lowerBound on x and y for generating random points
upperBnd = 100000	# upperBound on x and y for generating random points

class Point:
    def __init__(self, _x, _y, _label):
        self.x=_x
        self.y=_y
        self.label=_label

    def __getitem__(self, item):
        return (self.x, self.y, self.label)[item]

def getDist(a,b):
    return math.sqrt(pow(a.x-b.x,2)+pow(a.y-b.y,2))

def dispPoint(p):
    print "("+str(p.x)+","+str(p.y)+","+str(p.label)+")"

def genRandomPoint(lower, upper):
	return Point(random.uniform(lower, upper),random.uniform(lower, upper),random.randrange(0,C))
