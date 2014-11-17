import sys, math, random
import random
import myutils
from myutils import jobSize,lowerBnd,upperBnd,N,C
import mincemeat
import matplotlib
import matplotlib.pyplot as plt
import plot
def mapfn(k,ptSet):
    '''In the map step given a set of points as ptSet, it returns a 
    list of K nearest points to the query point q. q is not passed 
    explicity. It is passed as the last element of the ptSet.'''
    import sys, math,operator
    import myutils
    distList = [] 

    q = ptSet[-1]
    ptSet.pop()
    for p in ptSet:
        distList.append((p,myutils.getDist(p,q)))
    
    sortedDist = sorted(distList,key=operator.itemgetter(1))
    n=len(sortedDist)
    # print "Map"
    # print k
    # print sortedDist
    yield 0,sortedDist[0:min(n,myutils.K)]

def reducefn(k,vs):
    '''In the reduce function, we merge the k-nearest-point sets 
    returned by each client to get the global k nearest neighbours'''
    import sys, math,operator, heapq
    import myutils
    # print "Reduce"
    # print k
    # print vs

    maxHeap = [(p,-d) for (p,d) in vs[0]]
    heapq.heapify(maxHeap)

    for i in xrange(1,len(vs)):
        for e in vs[i]:
            if e[1]<(-1*maxHeap[0][1]):
                heapq.heappop(maxHeap)
                heapq.heappush(maxHeap,(e[0],-e[1]))

    return maxHeap

def test():
    ptSet = []
    ptSet.append(myutils.Point(1,0,0))
    ptSet.append(myutils.Point(20,0,0))
    ptSet.append(myutils.Point(5,0,0))
    ptSet.append(myutils.Point(2,0,0))
    ptSet.append(myutils.Point(10,0,0))
    return ptSet

def test2():
    ptSet = []
    ptSet.append(myutils.Point(-1,0,0))
    ptSet.append(myutils.Point(-2,0,0))
    ptSet.append(myutils.Point(-3,0,0))
    ptSet.append(myutils.Point(-4,0,0))
    return ptSet

def main():
    data=[]
    pts=[]
    q = myutils.genRandomPoint(lowerBnd, upperBnd)
    
    # ptSet = test()
    # ptSet.append(q)
    # data.append(ptSet)

    # ptSet2 = test2()
    # ptSet2.append(q)
    # data.append(ptSet2)
    jobs = (N+jobSize-1)/jobSize
    for x in xrange(0,jobs):
        ptSet = []
        for y in xrange(0,jobSize):
            p = myutils.genRandomPoint(lowerBnd, upperBnd)
            #ptSet.append(p)
            #pts.append(p)
            # myutils.dispPoint(rand)
        for y in xrange(0,jobSize/2):
            p = myutils.genRandomPtCircle(10000, (10,10), 1)
            ptSet.append(p)
            pts.append(p)
        for y in xrange(0,jobSize/2):
            p = myutils.genRandomPtCircle(10000, (-15000,-15000), 2)
            ptSet.append(p)
            pts.append(p)
        ptSet.append(q)
        data.append(ptSet)

    datasource = dict(enumerate(data))
    print "Done"

    s = mincemeat.Server()
    s.datasource = datasource
    s.mapfn = mapfn
    s.reducefn = reducefn
    results = s.run_server(password="changeme")

    freq = []
    for x in xrange(0,C):
        freq.append(0)

    for pt in results[0]:
        myutils.dispPoint(pt[0])
        freq[pt[0][2]] = freq[pt[0][2]]+1

    predClass = freq.index(max(freq))
    print predClass

    plot.plotGraph(pts,myutils.Point(q[0],q[1],predClass))

if __name__ == "__main__":
    main()
