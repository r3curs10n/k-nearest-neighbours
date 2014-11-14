import myutils
import matplotlib.pyplot as plt
import random
import pickle
colour = ['b','g','r','c','m','y']

def plotGraph(ptSet,q):
	for p in ptSet:
		plt.scatter(p[0],p[1],c=colour[p[2]])
	# plt.scatter(q[0],q[1],c=colour[q[2]],marker='x', linewidths=2)
	plt.scatter(q[0],q[1],c=colour[q[2]], marker='.', s = 700, linewidths=1)
	plt.show()

# def plotClusters(clusters):
# 	for i,c in enumerate(clusters):
# 	    print `c.centroid.coords[0]`+" : "+`c.centroid.coords[1]`
# 	    x = [temp.coords[0] for temp in c.points]
# 	    y = [temp.coords[1] for temp in c.points]
# 	    color = [random.uniform(0, 1.0) for i in range(3)]
# 	    plt.scatter(x,y,c=color)
# 	    plt.scatter([c.centroid.coords[0]],[c.centroid.coords[1]], marker='x', s = 500, linewidths=2)
# 	plt.show();

