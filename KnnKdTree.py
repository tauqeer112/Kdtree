import pprint
import random
import heapq
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# file is for all datapoints in training
K_nearest = []
file = "all_datapoints.txt"
testfile = "testfile.txt" #Testfile contains point for benchmark
alpha = 30 #alpha is the number of total points in the leaf node
fileindex = 0 #this if for naming the leafs.
generatefile = False #When set true all leaf nodes falling in a region will be written to a text file

#Loading the training data
f = open(file, "r")
datapoints = f.readlines()
points = []
for data in datapoints:
    tempdatapoints = [int(x) for x in data.split()]
    points.append(tempdatapoints)
f.close()

points = [tuple(x) for x in points]

#Loading the test Data
f = open(testfile, "r")
datapoints = f.readlines()
test_points = []
for data in datapoints:
    tempdatapoints = [int(x) for x in data.split()]
    test_points.append(tempdatapoints)
f.close()

test_points = [tuple(x) for x in test_points]


#This function xmax xmin ymax ymin , so that max spread can be selected
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

#find the axis to be used for dividing points or longest spread axis
def findaxis(rxmax , rxmin , rymax , rymin):
    x_spread = rxmax - rxmin
    y_spread = rymax - rymin
    if x_spread > y_spread :
        return 1
    else :
        return 2

#writes the leaf points to the log
def filelog(points):
    global fileindex
    with open("leaf"+str(fileindex)+".txt", 'w') as f:
        fileindex = fileindex + 1
        for point in points:
            f.write(str(point[0])+ " "+ str(point[1])+" "+str(point[2])+"\n")

#Builds the kd-tree when points are passed
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

#Builds small kd-tree when points are passed
def build_small_kdtree(points,d):

    n = len(points)

    if n <= d:
        # if generatefile is True:
        #     filelog(points)
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
            'left': build_small_kdtree(sorted_points[:n // 2 + 1],d),
            'right': build_small_kdtree(sorted_points[n // 2 + 1:],d)
        }



kd_tree = build_kdtree(points)

#Prints tree in user friendly manner
def pretty_KDTree(kdtree):
    print(bcolors.OKCYAN)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(kdtree)
    print(bcolors.ENDC)




#find distance between two points
def distance_squared(point1, point2):
    try:

        dx = point1[0] - point2[1]
        dy = point1[1] - point2[2]

        return (dx*dx + dy*dy)
    except:
        return float('inf')


#knn to find the K nearest neighbour using KD-TREE
def knn_kdtree(kd_tree, point, k, root=True):
    global K_nearest
    # if root is True:
    #     # print("assigning")
    #     K_nearest = [(float('-inf'), ()) for i in range(k+3)]
    if kd_tree['root'][0] == 'leaf':
        for data in kd_tree['root'][1]:
            if len(K_nearest) < k+3:
                distance = distance_squared(point, data)
                heapq.heappush(K_nearest, (-distance, data))
            # heapq.heapify(K_nearest)
            # K_nearest.sort()
            # print(K_nearest)
            else:
                max = K_nearest[0]
                current_max_dist = -max[0]
                curr_max_point = max[1]
                distance = distance_squared(point, data)
                if distance < current_max_dist:
                    heapq.heappushpop(K_nearest, (-distance, data))
                    # K_nearest[0] = (-distance, data)


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
        # K_nearest.sort()
        max = K_nearest[0]
        current_max_dist = -max[0]
        curr_max_point = max[1]

        if distance_squared(point, curr_max_point) > (point[axis - 1] - kd_tree['root'][0]):
            knn_kdtree(bad_branch, point, k, root=False)

        return K_nearest


#KNN to find K nearest neighbour using Brute Force
def knn_naive(points , point, k):
    listOfDistance = []
    for data in points:
        distance = distance_squared(point, data)
        listOfDistance.append((distance,data))
    # result = heapq.nsmallest(k,listOfDistance)
    listOfDistance.sort()
    return listOfDistance[:k]


# A function which checks wether output is consistent with brute force
def compareResult(knn_naive, knn_kdtree,k):
    knn_kdtree = [(-x[0], x[1]) for x in knn_kdtree]
    knn_naive.sort()
    knn_kdtree.sort()
    knn_kdtree = knn_kdtree[:k]
    print(bcolors.OKGREEN)
    print(knn_naive)
    print(knn_kdtree)
    print("\n")
    if all(i in knn_naive for i in knn_kdtree):
        print('Is KNN_KdTree result same as Knn Brute Force : True')
    else:
        print('Is KNN_KdTree result same as Knn Brute Force : False')
    print(bcolors.ENDC)



#
# point = (10,12)
#
# myK = knn_kdtree(kd_tree , point , 20)
# myKNaive = knn_naive(points, point, 20)

# compareResult(myKNaive, myK,20)

#for benchmarking kd Tree KNN with varying Number of data points
def bench_kd(test):
        kdtree = []
        log = []
        for i in range(1000,30000,2000):
            # print("inside")
            temp = build_kdtree(points[:i])
            kdtree.append(temp)

        j = 1000
        for kd in kdtree:
            start_time_kd= time.time()
            for t in test[:100]:
                knn_kdtree(kd, t, k=20, root=True)
            duration = time.time()-start_time_kd
            log.append([duration, j])
            j = j+2000

        print("Time Taken by Kdtree %s seconds ---", log)

#for benchmarking KNN Brute force with varying Number of data points
def bench_naive(test):
        log = []
        for i in range(1000,30000,2000):
            start_time_naive= time.time()
            for t in test[:100]:
                knn_naive(points[:i], t, k =20)
            duration = time.time()-start_time_naive
            log.append([duration, i])
        print("Time Taken by Naive %s seconds ---", log)

# bench_kd(test_points)
# bench_naive(test_points)

def bench_varying_kd_k(test):
    log = []
    list_of_K = [5, 20, 50, 100]
    for k in list_of_K:
        start_time_kd= time.time()
        for t in test[:1000]:
            knn_kdtree(kd_tree, t, k=k, root=True)
        duration = time.time()-start_time_kd
        log.append([duration, k])
    print("Time Taken by KD_TREE %s seconds ---", log)

def bench_varying_naive_k(test):
    log = []
    list_of_K = [5, 20, 50, 100]
    for k in list_of_K:
        start_time_kd= time.time()
        for t in test[:1000]:
            knn_naive(points, t, k)
        duration = time.time()-start_time_kd
        log.append([duration, k])
    print("Time Taken by Naive %s seconds ---", log)


def main():
    global kd_tree
    global points
    global K_nearest
    exit = False
    while(exit is False):
        print(bcolors.OKBLUE)
        K_nearest = []
        print("Enter Your choice \n")
        print("Enter 1. To find K nearest neighbour")
        print("Enter 2. See small Kd-Tree(n<=30)")
        print("Enter 3. To exit")
        choice = int(input("Enter your choice "))
        print(bcolors.ENDC)
        if choice == 3:
            exit = True
        elif choice == 1:
            k = int(input("Enter K value : "))
            x = int(input("Enter x co-ordinate : "))
            y = int(input("Enter y co-ordinate : "))
            start_time_kd= time.time()
            K_nearest_kd = knn_kdtree(kd_tree, (x,y), k, root=True)
            time_kd = time.time()-start_time_kd
            start_time_naive= time.time()
            K_nearest_naive = knn_naive(points,(x,y), k)
            time_naive = time.time()-start_time_naive
            compareResult(K_nearest_naive, K_nearest_kd, k)
            print(bcolors.OKCYAN)
            print("Time Taken by KD_Tree based KNN is" , time_kd, "\n")
            print("Time Taken by Brute force based KNN is" , time_naive, "\n")
            print(bcolors.ENDC)
        elif choice == 2:
            n = int(input("Enter n,first n number of points will be built kd_tree: "))
            d = int(input("Enter alpha : "))
            mykdtree = build_small_kdtree(points[:n],d)
            pretty_KDTree(mykdtree)
        else:
            print("Wrong Input \n")



main()
# print("alpha = ", alpha)
# bench_varying_kd_k(test_points)
# bench_varying_naive_k(test_points)
