def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of 'h' tuples
         [(u0,v0), (u1,v1), ...]  
    """
    #Your implementation goes here
    min_point = listPts[0]
    for p in range(len(listPts)):
        if listPts[p][1] < min_point[1]:
            min_point = listPts[p]
        elif listPts[p][1] == min_point[1]:
            if listPts[p][0] > min_point[0]:
                min_point = listPts[p]
    newList = []
    newList.append(min_point)
    for n in range(0, len(listPts)):
        if listPts[n] != min_point:
            newList.append((listPts[n][0], listPts[n][1], theta(min_point, listPts[n])))
   # print("newlist")
   # print(newList)
    l = sorted(newList[1:], key=lambda x: theta(x, min_point))
  #  print("ordered_list")
  #  print(l)   
    s = []
    s.append(min_point)
    s.append(l[0])
    s.append(l[1])
    points = l[2:]
  #  print("points")
   # print(points)
    for j in range(0, len(points)):
   #     print("new point")
    #    print(points[j])      
     #   print("stack")
      #  print(s)
        while not (isCCW(s[-2], s[-1], points[j])):
     #       print("not ccw")
            s.pop()
      #      print("after pop stack")
       #     print(s)
        s.append(points[j])
    chull = []
    for k in range(len(s)):
        chull.append((s[k][0], s[k][1]))
    return chull

listPts = readDataPts("Set_B.dat", 500)
print(grahamscan(listPts))
print(len(grahamscan(listPts)))