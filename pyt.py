import pprint
import random
import numpy as np
import heapq
import time

file = "all_datapoints.txt"
testfile = "testfile.txt"
alpha = 30
fileindex = 0
generatefile = False


f = open(file, "r")
datapoints = f.readlines()
points = []
for data in datapoints:
    tempdatapoints = [int(x) for x in data.split()]
    points.append(tempdatapoints)
f.close()

points = [tuple(x) for x in points]

f = open(testfile, "r")
datapoints = f.readlines()
test_points = []
for data in datapoints:
    tempdatapoints = [int(x) for x in data.split()]
    test_points.append(tempdatapoints)
f.close()

test_points = [tuple(x) for x in test_points]

def findmaxrange(datapoints):

    rxmax = datapoints[0][1]
    rymax = datapoints[0][2]
    rxmin = datapoints[0][1]
    rymin = datapoints[0][2]
    for data in datapoints:
        if data[1] > rxmax :
            rxmax = data[0]
        if data[1] < rxmin :
            rxmin = data[0]
        if data[2] > rymax :
            rymax = data[1]
        if data[2] < rymin :
            rymin = data[1]
    return rxmax , rxmin , rymax , rymin

def findaxis(rxmax , rxmin , rymax , rymin):
    x_spread = rxmax - rxmin
    y_spread = rymax - rymin
    if x_spread > y_spread :
        return 1
    else :
        return 2

def filelog(points):
    global fileindex
    with open("leaf"+str(fileindex)+".txt", 'w') as f:
        fileindex = fileindex + 1
        for point in points:
            f.write(str(point[0])+ " "+ str(point[1])+" "+str(point[2])+"\n")

def build_kdtree(points):
    global alpha
    n = len(points)

    if n <= alpha:
        if generatefile is True:
            filelog(points)
        return {"root" : ["leaf",points],
                 "left" : None,
                 "right" : None

        }
    else:
        rxmax , rxmin , rymax , rymin = findmaxrange(points)
        axis = findaxis(rxmax, rxmin, rymax, rymin)
        # print(rxmax , rxmin , rymax , rymin)
        sorted_points = sorted(points, key=lambda point: point[axis])
        # roots.append([sorted_points[n // 2][axis], axis])

        return {
            'root': [sorted_points[n // 2][axis], axis],
            'left': build_kdtree(sorted_points[:n // 2 + 1]),
            'right': build_kdtree(sorted_points[n // 2 + 1:])
        }



kd_tree = build_kdtree(points)

pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(kd_tree)


def distance_squared(point1, point2):
    try:

        dx = point1[0] - point2[1]
        dy = point1[1] - point2[2]

        return (dx*dx + dy*dy)
    except:
        return float('inf')


def compare(point , point1 , point2):
    d1 = distance_squared(point , point1)
    d2 = distance_squared(point , point2)

    if d1 > d2:
        return d2, point2
    else:
        return d1, point1


K_nearest = []

def knn_kdtree(kd_tree, point, k, root=True):
    global K_nearest
    if root is True:
        # print("assigning")
        K_nearest = [(float('-inf'), ()) for i in range(k+3)]

    if kd_tree['root'][0] == 'leaf':
        for data in kd_tree['root'][1]:
            # heapq.heapify(K_nearest)
            K_nearest.sort()
            # print(K_nearest)
            max = K_nearest[0]
            current_max_dist = -max[0]
            curr_max_point = max[1]
            distance = distance_squared(point, data)
            if distance < current_max_dist:
                # heapq.heappushpop(K_nearest, (-distance, data))
                K_nearest[0] = (-distance, data)


    else:
        axis = kd_tree['root'][1]
        good_branch = None
        bad_branch = None

        if point[axis - 1] < kd_tree['root'][0]:
            good_branch = kd_tree['left']
            bad_branch = kd_tree['right']
        else:
            good_branch = kd_tree['right']
            bad_branch = kd_tree['left']

        knn_kdtree(good_branch, point, k, root=False)

        # heapq.heapify(K_nearest)
        K_nearest.sort()
        max = K_nearest[0]
        current_max_dist = -max[0]
        curr_max_point = max[1]

        if distance_squared(point, curr_max_point) > (point[axis - 1] - kd_tree['root'][0]):
            knn_kdtree(bad_branch, point, k, root=False)

        return K_nearest



def knn_naive(points , point, k):
    listOfDistance = []
    for data in points:
        distance = distance_squared(point, data)
        listOfDistance.append((distance,data))
    # result = heapq.nsmallest(k,listOfDistance)
    listOfDistance.sort()
    return listOfDistance[:k]


def compareResult(knn_naive, knn_kdtree,k):
    knn_kdtree = [(-x[0], x[1]) for x in knn_kdtree]
    knn_naive.sort()
    knn_kdtree.sort()
    knn_kdtree = knn_kdtree[:k]
    print(knn_naive)
    print(knn_kdtree)
    if all(i in knn_naive for i in knn_kdtree):
        print('True')
    else:
        print('False')




# point = (10,12)
#
# myK = knn_kdtree(kd_tree , point , 24)
# myKNaive = knn_naive(points, point, 24)
#
# compareResult(myKNaive, myK,20)

def bench_kd(test):
        log = []
        kdtree1 = build_kdtree(points[:1000])
        kdtree2 = build_kdtree(points[:5000])
        kdtree3 = build_kdtree(points[:10000])
        kdtree4 = build_kdtree(points[:30000])
        start_time_kd= time.time()
        for t in test[:100]:
            knn_kdtree(kdtree1, t, k =10, root=True)
        duration = time.time()-start_time_kd
        log.append([duration, "kd1"])
        start_time_kd = time.time()
        for t in test[:100]:
            knn_kdtree(kdtree2, t, k=10, root=True)
        duration = time.time()-start_time_kd
        log.append([duration, "kd2"])
        start_time_kd = time.time()
        for t in test[:100]:
            knn_kdtree(kdtree3, t, k=10, root=True)
        duration = time.time()-start_time_kd
        log.append([duration, "kd3"])
        start_time_kd = time.time()
        for t in test[:100]:
            knn_kdtree(kdtree4, t, k=10, root=True)
        duration = time.time()-start_time_kd
        log.append([duration, "kd4"])

        # start_time_kd = time.time()
        # for t in test:
        #     knn_kdtree(kd_tree, t, k=10, root=True)
        # duration = time.time()-start_time_kd
        # log.append([duration, len(test)])
        # start_time_kd = time.time()

        print("Time Taken by Kdtree %s seconds ---", log)

def bench_naive(test):
        log = []
        start_time_kd= time.time()
        for t in test[:100]:
            knn_naive(points[:1000], t, k =40)
        duration = time.time()-start_time_kd
        log.append([duration, 1000])
        for t in test[:100]:
            knn_naive(points[:5000], t, k =40)
        duration = time.time()-start_time_kd
        log.append([duration, 5000])
        for t in test[:100]:
            knn_naive(points[:10000], t, k =40)
        duration = time.time()-start_time_kd
        log.append([duration, 10000])
        for t in test[:100]:
            knn_naive(points[:30000], t, k =40)
        duration = time.time()-start_time_kd
        log.append([duration, 30000])
        # start_time_kd = time.time()
        # for t in test:
        #     knn_naive(points, t, k =10)
        # duration = time.time()-start_time_kd
        # log.append([duration, len(test)])

        print("Time Taken by Naive %s seconds ---", log)

bench_kd(test_points)
bench_naive(test_points)
