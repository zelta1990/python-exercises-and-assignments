"""
   Convex Hull Assignment: COSC262 (2017)
   Student Name: Xiaoshi Xie
   Usercode: 22378644
"""
import time 

def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]
    """
    pts = []
    file = open(filename,"r")
    for i in range(0,N):
        line = file.readline()
        tmp = line.split(" ")
        pts.append((float(tmp[0]), float(tmp[1])))        
    return pts

def theta(ptA, ptB):
    """ Computes an approximation of the angle between
     the line AB and a horizontal line through A.
     """    
    dx = ptB[0] - ptA[0]
    dy = ptB[1] - ptA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0
    else:
        t = 1 * dy/(abs(dx) + abs(dy))
    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = 4 + t
    if t == 0:
        return 360
    else:
        return t * 90
    
    
def get_distance(pointA, pointB):
    "return the distance between two given vertices"
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    d = (dx**2+dy**2)**(1/2)
    return d
    


def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          giftwrap algorithm as a list of 'h' tuples
          [(u0,v0), (u1,v1), ...]    
    """
    #Your implementation goes here
    start_time = time.time()    
    min_point = listPts[0]
    for p in range(len(listPts)):
        if listPts[p][1] < min_point[1]:
            min_point = listPts[p]
            k = p
        elif listPts[p][1] == min_point[1]:
            if listPts[p][0] > min_point[0]:
                min_point = listPts[p]
                k = p
    v = 0
    i = 0
    listPts.append(min_point)    
    n = len(listPts) -1
    result = []
    while k != n:
        listPts[i], listPts[k] = listPts[k], listPts[i]
        result.append(listPts[i])
        minAngle = 361
        for j in range(i+1, n+1):
            angle = theta(listPts[i], listPts[j])
            if angle < minAngle and angle > v and listPts[j] != listPts[i]:
                minAngle = angle
                k = j
            elif angle == minAngle:
                if get_distance(listPts[i], listPts[j]) > get_distance(listPts[i], listPts[k]):
                    minAngle = angle
                    k = j
                
        i = i + 1
        v = minAngle    
    time_consumed = time.time() - start_time
                       
    return time_consumed


def isCCW(ptA, ptB, ptC):
    #return true if point A, B, C are in clockwise order#
    l = (ptB[0] - ptA[0]) * (ptC[1] - ptA[1]) - (ptB[1] - ptA[1]) * (ptC[0]-ptA[0])
    return l > 0
    


def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of 'h' tuples
         [(u0,v0), (u1,v1), ...]  
    """
    #Your implementation goes here
    start_time = time.time()    
    
    min_point = listPts[0]
    for p in range(len(listPts)):
        if listPts[p][1] < min_point[1]:
            min_point = listPts[p]
        elif listPts[p][1] == min_point[1]:
            if listPts[p][0] > min_point[0]:
                min_point = listPts[p]
    newList = []
    points = []
    newList.append(min_point)
    for n in range(0, len(listPts)):
        if listPts[n] != min_point:
            points.append((listPts[n][0], listPts[n][1], theta(min_point, listPts[n])))
    ordered_byX_list = sorted(points, key=lambda x: x[0])
    ordered_byY_list = sorted(ordered_byX_list, key=lambda x: x[1])    
    newList += ordered_byY_list
    l = sorted(newList[1:], key=lambda x: theta(min_point, x)) 
    s = []
    s.append(min_point)
    s.append(l[0])
    s.append(l[1])
    points = l[2:]
    for j in range(0, len(points)):
        while not (isCCW(s[-2], s[-1], points[j])):
            s.pop()
        s.append(points[j])
    chull = []
    for k in range(len(s)):
        chull.append((s[k][0], s[k][1]))
    time_consumed = time.time() - start_time
    
    return time_consumed

"""quick hull implementation"""

def get_extreme_pts(listPts): #return the lowest and leftmost point and the highest and rightmost point
    ordered_byY_list = sorted(listPts, key=lambda x: x[1])
    ordered_byX_list = sorted(ordered_byY_list, key=lambda x: x[0])
    min_point = ordered_byX_list[0]
    max_point = ordered_byX_list[len(listPts)-1]
    return min_point, max_point

def get_left_pts(min_point, max_point, listPts):#return the list of points lying on the left side of line joined by min and max
    left_pts = []
    for p in listPts:
        if isCCW(min_point, max_point, p):
            left_pts.append(p)
    return left_pts

def find_distance(ptA, ptB, ptC): # find the proportional distance from ptC to the line joining ptA and ptB
    result = abs((ptC[1]-ptA[1])*(ptB[0]- ptA[0])-(ptB[1]-ptA[1])*(ptC[0]-ptA[0]))
    return result


def quickhull(listPts, min_point, max_point):
    left_pts = get_left_pts(min_point, max_point, listPts)
    max_dist = 0
    far_point = []
    chull = []
    for p in left_pts:
        if p != min_point and p != max_point:
            dist = find_distance(min_point, max_point, p)
            if dist > max_dist:
                max_dist = dist
                far_point = p    
    if len(far_point) == 0:
        chull.append(max_point)
        return chull
    upperhull = quickhull(left_pts, min_point, far_point)
    lowerhull = quickhull(left_pts, far_point, max_point)
    chull = upperhull + lowerhull
    return chull


def amethod(listPts):     
    """Returns the convex hull vertices computed using 
          a third algorithm
    """    
    start_time = time.time()    
    
    min_point, max_point = get_extreme_pts(listPts)
    upperhull = quickhull(listPts, min_point, max_point)
    lowerhull = quickhull(listPts, max_point, min_point)
    result = upperhull + lowerhull
    time_consumed =  time.time() - start_time   
    return time_consumed


    
def main():
    giftwrap_time = []    
    graham_time = []
    amethod_time = []
    for step in range(2000, 32000, 2000):
        listPts = readDataPts('Set_A.dat', step)            
        giftwrap_time.append(giftwrap(listPts))
        graham_time.append(grahamscan(listPts))
        amethod_time.append(amethod(listPts))
    print(giftwrap_time)
    print(graham_time)
    print(amethod_time)
 
if __name__  ==  "__main__":
    main()
  