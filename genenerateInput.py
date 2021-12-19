import random
f = open("input.txt", 'w')
f.close()
f = open("input.txt", 'a')
for i in range(0, 10000):
    data = ""
    data = data + str(random.randint(0,401)) + " "
    data = data + str(random.randint(0,401)) + "\n"
    f.write(data)


# f = open("input.txt", "r")
# datapoints = f.readlines()
# mydatapoints = []
# for data in datapoints:
#     tempdatapoints = [int(x) for x in data.split()]
#     mydatapoints.append(tempdatapoints)
#
# points =[]
#
# for point in mydatapoints:
#     points.append([point[1], point[2]])
#
#
# dim = 2
#
#
#
#
# def findmaxrange(datapoints):
#     rxmax = datapoints[0][1]
#     rymax = datapoints[0][2]
#     rxmin = datapoints[0][1]
#     rymin = datapoints[0][2]
#     for data in mydatapoints:
#         if data[1] > rxmax :
#             rxmax = data[1]
#         if data[1] < rxmin :
#             rxmin = data[1]
#         if data[2] > rymax :
#             rymax = data[1]
#         if data[2] < rymin :
#             rymin = data[1]
#         return rxmax , rxmin , rymax , rymin
#
# print(findmaxrange(mydatapoints))
#
# def findaxis(rxmax , rxmin , rymax , rymin):
#     x_spread = rxmax - rxmin
#     y_spread = rymax - rymin
#     if x_spread > y_spread :
#         return 1
#     else :
#         return 2
#
#
#
#
# # Makes the KD-Tree for fast lookup
# def make_kd_tree(points, dim =2 , i=1):
#     if len(points) <=3:
#         return ["leaf",points]
#     elif len(points) > 3:
#         rxmax , rxmin , rymax , rymin = findmaxrange(points)
#         i = findaxis(rxmax , rxmin , rymax , rymin)
#         points.sort(key=lambda x: x[i])
#         half = len(points) >> 1
#         return [
#
#             make_kd_tree(points[: half+1] , dim, i),
#             make_kd_tree(points[half + 1:], dim, i),
#             ['root',i,points[half]]
#
#         ]
#
# def make_kd_tree_2(points, dim, i=0):
#     if len(points) > 1:
#         points.sort(key=lambda x: x[i])
#         i = (i + 1) % dim
#         half = len(points) >> 1
#         return [
#             make_kd_tree_2(points[: half], dim, i),
#             make_kd_tree_2(points[half + 1:], dim, i),
#             points[half]
#         ]
#     elif len(points) == 1:
#         return [None, None, points[0]]
#
# kd_tree  = make_kd_tree(mydatapoints)
# kd_tree2 = make_kd_tree_2(points , 2)
#
# print(kd_tree)
#
# def dist_sq(a, b):
#     print(a , b)
#     res = sum((a[i] - b[2][i+1]) ** 2 for i in range(0,2))
#     print(res)
#     return res
#
# # def dist_sq_dim(a, b):
# #     return dist_sq(a, b, dim)
#
# result1 = []

# test = [[2,3]]
#
# for tree in kd_tree:
#     print(tree)
#     print("\n")
