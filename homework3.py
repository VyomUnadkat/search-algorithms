#importing the libraries
from queue import Queue, PriorityQueue
import time
import math
import os
#getting the values from input.txt
my_input = []
inputt = []
with open('input.txt') as input:
    for line in input:
        line = line.rstrip()
        my_input.append(line)

for words in my_input:
    words = words.split(' ')
    inputt.append(words)


algo = inputt[0][0]
height = int(inputt[1][0])
width = int(inputt[1][1])
start_year = int(inputt[2][0])
start_x = int(inputt[2][1])
start_y = int(inputt[2][2])
end_year = int(inputt[3][0])
end_x = int(inputt[3][1])
end_y = int(inputt[3][2])
no_of_channels = int(inputt[4][0])

#creating a graph inclusive of the jaunt years
graph1 = {}

for i in inputt[5:5+no_of_channels]:
    if (int(i[0]),int(i[1]),int(i[2])) in graph1:
        if int(i[0]) != int(i[3]):
            graph1[(int(i[0]),int(i[1]),int(i[2]))].append((int(i[3]),int(i[1]),int(i[2])))
    else:
        graph1[(int(i[0]),int(i[1]),int(i[2]))] = [(int(i[3]),int(i[1]),int(i[2]))]
    #graph1[(int(i[0]),int(i[1]),int(i[2]))] = [(int(i[3]),int(i[1]),int(i[2]))]
    if (int(i[3]),int(i[1]),int(i[2])) in graph1:
        if int(i[0]) != int(i[3]):
            graph1[(int(i[3]),int(i[1]),int(i[2]))].append((int(i[0]),int(i[1]),int(i[2])))
    else:
        graph1[(int(i[3]),int(i[1]),int(i[2]))] = [(int(i[0]),int(i[1]),int(i[2]))]
    #graph1[(int(i[3]),int(i[1]),int(i[2]))] = [(int(i[0]),int(i[1]),int(i[2]))]

#initialising dictionaries and queues
print(graph1)

file1 = open('output.txt', 'w')
#file1.write("Now the file has more content!")
#filetowrite.close()

#open and read the file after the appending:

came_from = {}
cost_so_far = {}
if algo == "BFS":
    queue = Queue()
else:
    queue = PriorityQueue()

#heuristic function: euclidian distance
def heuristic(a, b):

    ax = a[0]
    ay = a[1]
    az = a[2]
    bx = b[0]
    by = b[1]
    bz = b[2]
    return math.sqrt(abs((ax - bx) ** 2 + (az - bz) ** 2 + (ay - by) ** 2))

#a* algo
def astar_sp(graph, a, b):
    yr1 = a[0]
    x1 = a[1]
    y1 = a[2]
    yr2 = b[0]
    x2 = b[1]
    y2 = b[2]

    queue.put((0, [(yr1, x1, y1)]))
    came_from[(yr1, x1, y1)] = None
    cost_so_far[(yr1, x1, y1)] = 0


    if (yr1, x1, y1) == (yr2, x2, y2):
        return (0,[a, b])

    if x2 > height or y2 > width:
        #print('FAIL')
        file1.write("FAIL\n")
        exit()

    while not queue.empty():
        s = queue.get()
        #print(s)

        cost, node = s
        #print('cost')
        #print(cost)
        #print('node')
        #print(node)
        #print(node[-1])
        yrn, x, y = node[-1]
        #print(x)
        #print(y)

        if (yrn,x,y) == b:
            return s
        moves = [(yrn, x+1, y), (yrn, x+1, y+1), (yrn, x+1, y-1), (yrn, x-1,y), (yrn, x-1, y-1), (yrn, x-1, y+1), (yrn, x, y+1), (yrn, x, y-1)]
        if (yrn, x, y) in graph:
            moves.insert(0,graph[(yrn,x,y)][0])

        for (yr, m, n) in moves:

            if abs(x - m) + abs(y - n) == 2:
                cos = 14
            elif abs(x - m) + abs(y - n) == 1:
                cos = 10
            else:
                cos = abs(yrn - yr)



            new_cost = cost_so_far[(yrn,x,y)] + cos
            if (0 <= m < height and 0 <= n < width) and ((yr,m,n) not in cost_so_far or new_cost < cost_so_far[(yr,m,n)]):
                cost_so_far[(yr,m,n)] = new_cost
                priority = new_cost + heuristic((yr2,x2,y2), (yr,m,n))
                queue.put((priority, node + [(yr,m,n)]))
                came_from[(yr,m,n)] = (yrn,x,y)
    #print("FAIL")
    file1.write("FAIL\n")
    file1.close()
    exit()

def bfs_sp(graph, a, b):
    yr1 = a[0]
    x1 = a[1]
    y1 = a[2]
    yr2 = b[0]
    x2 = b[1]
    y2 = b[2]

    queue.put([(yr1, x1, y1)])
    came_from[(yr1, x1, y1)] = None


    if (yr1, x1, y1) == (yr2, x2, y2):
        return a,b

    if x2 > height or y2 > width:
        #print('FAIL')
        file1.write("FAIL\n")
        exit()

    while not queue.empty():
        s = queue.get()
        #print(s)

        node = s

        yrn, x, y = node[-1]


        if (yrn,x,y) == b:
            return s

        moves = [(yrn, x+1, y), (yrn, x+1, y+1), (yrn, x+1, y-1), (yrn, x-1,y), (yrn, x-1, y-1), (yrn, x-1, y+1), (yrn, x, y+1), (yrn, x, y-1)]
        if (yrn, x, y) in graph:
            moves.insert(0,graph[(yrn,x,y)][0])
        for (yr, m, n) in moves:
            if 0 <= m < height and 0 <= n < width and (yr,m,n) not in came_from:
                queue.put((s + [(yr,m,n)]))
                came_from[(yr,m,n)] = (yrn,x,y)
    #print('FAIL')
    file1.write("FAIL\n")
    file1.close()
    exit()

def ucs_sp(graph, a, b):
    yr1 = a[0]
    x1 = a[1]
    y1 = a[2]
    yr2 = b[0]
    x2 = b[1]
    y2 = b[2]

    queue.put((0, [(yr1, x1, y1)]))
    came_from[(yr1, x1, y1)] = None
    cost_so_far[(yr1, x1, y1)] = 0


    if (yr1, x1, y1) == (yr2, x2, y2):
        return (0,[a, b])

    if x2 > height or y2 > width:
        #print('FAIL')
        file1.write("FAIL\n")
        exit()

    while not queue.empty():
        s = queue.get()
        #print(s)

        cost, node = s
        #print('cost')
        #print(cost)
        #print('node')
        #print(node)
        #print(node[-1])
        yrn, x, y = node[-1]
        #print(x)
        #print(y)

        if (yrn,x,y) == b:
            return s
        moves = [(yrn, x+1, y), (yrn, x+1, y+1), (yrn, x+1, y-1), (yrn, x-1,y), (yrn, x-1, y-1), (yrn, x-1, y+1), (yrn, x, y+1), (yrn, x, y-1)]
        if (yrn, x, y) in graph:
            moves.insert(0,graph[(yrn,x,y)][0])

        for (yr, m, n) in moves:

            if abs(x - m) + abs(y - n) == 2:
                cos = 14
            elif abs(x - m) + abs(y - n) == 1:
                cos = 10
            else:
                cos = abs(yrn - yr)



            new_cost = cost_so_far[(yrn,x,y)] + cos
            if 0 <= m < height and 0 <= n < width and ((yr,m,n) not in cost_so_far or new_cost < cost_so_far[(yr,m,n)] or (yr,m,n) not in came_from):
                cost_so_far[(yr,m,n)] = new_cost
                priority = new_cost
                queue.put((priority, node + [(yr,m,n)]))
                came_from[(yr,m,n)] = (yrn,x,y)
    #print("FAIL")
    file1.write("FAIL\n")
    file1.close()
    exit()

def cal_count_bfs(q):
    cost_list = [0]
    cost = 1
    #print('im in func cal count')
    for i in range(len(q)-1):
        #print(i)
        cost_list.append(cost)
    #print('final length', len(q))
    #print('cost list')
    #print(cost_list)
    return cost_list

def cal_count_ucs(q):
    cost_list = [0]

    for i in range(1,len(q)):

        if abs(q[i][1] - q[i-1][1]) + abs(q[i][2] - q[i-1][2]) == 2:
            cost = 14
        elif abs(q[i][1] - q[i-1][1]) + abs(q[i][2] - q[i-1][2]) == 1:
            cost = 10
        else:
            cost = abs(q[i][0] - q[i-1][0])

        cost_list.append(cost)

    return cost_list

if algo == "BFS":
    starttime = time.time()
    fa = bfs_sp(graph1, (start_year,start_x,start_y), (end_year,end_x,end_y))
    #print(fa)
    #print("This is final answer")
    #print(len(fa))
    if (start_year,start_x,start_y) == (end_year,end_x,end_y):
        cost_lis_final = [0]
    else:
        cost_lis_final = cal_count_bfs(fa)

    #print('this is the cost sum')
    #print(sum(cost_lis_final))
    file1.write(str(sum(cost_lis_final))+'\n')

    if (start_year,start_x,start_y) == (end_year,end_x,end_y):
        #print(len(fa)-1)
        file1.write(str(len(fa)-1)+'\n')
        for i in range(len(fa)-1):
                #print("{}\t{}\t{}\t{}".format(fa[i][0],fa[i][1],fa[i][2],cost_lis_final[i]))
                file1.write("{} {} {} {}\n".format(fa[i][0],fa[i][1],fa[i][2],cost_lis_final[i]))
    else:
        #print(len(fa))
        file1.write(str(len(fa))+'\n')
        for i in range(len(fa)):
                #print("{}\t{}\t{}\t{}".format(fa[i][0],fa[i][1],fa[i][2],cost_lis_final[i]))
                file1.write("{} {} {} {}\n".format(fa[i][0],fa[i][1],fa[i][2],cost_lis_final[i]))

    #endtime = time.time()
    #print('timestamp=', endtime - starttime)
    #file1.write(str(endtime - starttime)+'\n')
    file1.close()

elif algo == "UCS":
    starttime = time.time()
    fa = ucs_sp(graph1, (start_year,start_x,start_y), (end_year,end_x,end_y))


    cost_lis_final = cal_count_ucs(fa[1])
    #print(sum(cost_lis_final))
    file1.write(str(sum(cost_lis_final))+'\n')

    if (start_year,start_x,start_y) == (end_year,end_x,end_y):
        #print(len(fa[1])-1)
        file1.write(str(len(fa[1])-1)+'\n')
        for i in range(len(fa[1])-1):
                #print("{}\t{}\t{}\t{}".format(fa[1][i][0],fa[1][i][1],fa[1][i][2],cost_lis_final[i]))
                file1.write("{} {} {} {}\n".format(fa[1][i][0],fa[1][i][1],fa[1][i][2],cost_lis_final[i]))
    else:
        #print(len(fa[1]))
        file1.write(str(len(fa[1]))+'\n')
        for i in range(len(fa[1])):
                #print("{}\t{}\t{}\t{}".format(fa[1][i][0],fa[1][i][1],fa[1][i][2],cost_lis_final[i]))
                file1.write("{} {} {} {}\n".format(fa[1][i][0],fa[1][i][1],fa[1][i][2],cost_lis_final[i]))

    #endtime = time.time()

    #print('timestamp=', endtime - starttime)
    #file1.write(str(endtime - starttime)+'\n')
    file1.close()

elif algo == "A*":
    starttime = time.time()
    fa = astar_sp(graph1, (start_year,start_x,start_y), (end_year,end_x,end_y))


    cost_lis_final = cal_count_ucs(fa[1])
    #print(sum(cost_lis_final))
    file1.write(str(sum(cost_lis_final))+'\n')

    if (start_year,start_x,start_y) == (end_year,end_x,end_y):
        #print(len(fa[1])-1)
        file1.write(str(len(fa[1])-1)+'\n')
        for i in range(len(fa[1])-1):
                #print("{}\t{}\t{}\t{}".format(fa[1][i][0],fa[1][i][1],fa[1][i][2],cost_lis_final[i]))
                file1.write("{} {} {} {}\n".format(fa[1][i][0],fa[1][i][1],fa[1][i][2],cost_lis_final[i]))
    else:
        #print(len(fa[1]))
        file1.write(str(len(fa[1]))+'\n')
        for i in range(len(fa[1])):
                #print("{}\t{}\t{}\t{}".format(fa[1][i][0],fa[1][i][1],fa[1][i][2],cost_lis_final[i]))
                file1.write("{} {} {} {}\n".format(fa[1][i][0],fa[1][i][1],fa[1][i][2],cost_lis_final[i]))

    endtime = time.time()

    #print('timestamp=', endtime - starttime)
    #file1.write(str(endtime - starttime)+'\n')
    file1.close()
else:
    #print("FAIL")
    file1.write("FAIL\n")
    file1.close()

    exit()
