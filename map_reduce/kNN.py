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
    yield 0,sortedDist[0:min(n,myutils.K)]

def reducefn(k,vs):
    '''In the reduce function, we merge the k-nearest-point sets 
    returned by each client to get the global k nearest neighbours'''
    import sys, math,operator, heapq
    import myutils

    maxHeap = [(p,-d) for (p,d) in vs[0]]
    heapq.heapify(maxHeap)

    for i in xrange(1,len(vs)):
        for e in vs[i]:
            if e[1]<(-1*maxHeap[0][1]):
                heapq.heappop(maxHeap)
                heapq.heappush(maxHeap,(e[0],-e[1]))

    return maxHeap

def main():
    data=[]
    pts=[]
    # q = myutils.genRandomPoint(lowerBnd, upperBnd)
    q = myutils.Point(500,500,0)
    
    # ****************
    # all points randomly generated
    # ****************
    # jobs = (N+jobSize-1)/jobSize
    # for x in xrange(0,jobs):
    #     ptSet = []
    #     for y in xrange(0,jobSize):
    #         p = myutils.genRandomPoint(lowerBnd, upperBnd)
    #         ptSet.append(p)
    #         pts.append(p)
    #         # myutils.dispPoint(rand)
    #     ptSet.append(q)
    #     data.append(ptSet)


    # ****************
    # 3 almost circular clusters with random points
    # ****************
    jobs = (N+jobSize-1)/jobSize
    for x in xrange(0,jobs):
        ptSet = []
        for y in xrange(0,5*jobSize/12):
            p = myutils.genRandomPtCircle(10000, myutils.Point(10,10,-1), 1)
            ptSet.append(p)
            pts.append(p)
        for y in xrange(0,5*jobSize/12):
            p = myutils.genRandomPtCircle(10000, myutils.Point(-15000,-15000,-1), 2)
            ptSet.append(p)
            pts.append(p)
        for y in xrange(0,jobSize/6):
            p = myutils.genRandomPtCircle(1000, myutils.Point(100,100,-1), 0)
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
