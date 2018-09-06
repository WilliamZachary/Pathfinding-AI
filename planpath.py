import argparse as ap
import re
import platform
from Node import Node
import timeit

######## RUNNING THE CODE ####################################################
#   You can run this code from terminal by executing the following command
#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag> <algorithm>
#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0 A
#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA
###############################################################################


################## YOUR CODE GOES HERE ########################################

def neighborExists(current, size, direction):
    if current[0] + direction[0] >= 0 and current[0] + direction[0] < size and current[1] + direction[1] >= 0and current[1] + direction[1] < size:
        return True
    else:
        return False

# return potential childrens (M) if (not mountain, not diagonal mountain neighbor, non ancestor) and put current into closed
def expandNode(nodeMap, current, closed, directions, idNumber, bound):

    currentID= idNumber

    x= current.coordinate[0]
    y= current.coordinate[1]
    children= None
    operations= ['U', 'RU', 'R', 'RD', 'D', 'LD', 'L', 'LU']

    potentialChildren= []

    # For every directions
    for index in range(len(directions)):

        # if A* algorithm, bound is -1, skip the checking
        if bound != -1:
            # if depth == bound, set the node to closed and quit the expansion
            if current.getDepth() == bound:
                break

        # Check if neighbor exists
        if not neighborExists([x,y], len(nodeMap), directions[index]):
            continue

        children= nodeMap[y+directions[index][1]][x+directions[index][0]]

        # Check if its not a mountain
        if children.isMountain():
            continue
        # Check if not a diagonal mountain neighbor
        if (index % 2) != 0 and children.isMountNeighbor():
            continue
        # Check if ancestor
        if children.isClosed():
            continue

        newValue = current.getActual()
        # Found the new cost
        # If a diagonal children
        if (index % 2) != 0:
            newValue+= 1
        # If a vertical or horizontal children
        else:
            newValue+= 2

        # if not in graph add it
        if not children.inGraphAlr():
            children.setDepth(current.getDepth() + 1)

            currentID+= 1
            identifier= 'N'+ str(currentID)
            children.setIdentifier(identifier)
            children.putInGraph()

            children.setOperator(operations[index])
            children.setActual(newValue)
            current.addChildren(children)
            children.setParent(current)
            potentialChildren.append(children)

        # Update the actual cost if its in graph and more expensive
        elif children.inGraphAlr() and children.getActual() > newValue:
            children.setDepth(current.getDepth() + 1)

            children.setOperator(operations[index])
            children.setActual(newValue)
            current.addChildren(children)
            children.setParent(current)
            potentialChildren.append(children)

    # Put node in closed
    current.closeNode()
    closed.append(current)

    return potentialChildren, currentID

def processMap(map):

    realMap= []

    # Get the size of the map
    size= map[0].split('\n')
    size= int(size[0])

    # Turn string into array of chars
    for i in range(size):
        temp = list(map[i + 1])
        if temp[len(temp)-1] is '\n':
            temp.pop()
        realMap.append(temp)

    nodeMap = []

    start = None
    goal = None

    # Turn map into a map of nodes
    for y in range(len(realMap)):
        temp = []
        for x in range(len(realMap)):
            isMountain = False
            if realMap[y][x] == 'X':
                isMountain = True

            node = Node(isMountain, x, y)
            temp.append(node)

            if realMap[y][x] == 'G':
                node.designateGoal()
                goal = node

            if realMap[y][x] == 'S':
                start = node
        nodeMap.append(temp)

    return nodeMap, start, goal

# Mark every mountains
def markMountain(nodeMap,directions):
    # Designate mountain vertical and horitzontal neighbors
    size= len(nodeMap)

    for y in range(size):
        for x in range(size):
            if nodeMap[y][x].isMountain():
                for index in [0, 2, 4, 6]:
                    direction = directions[index]
                    if neighborExists([x, y], size, direction):
                        nodeMap[y + direction[1]][x + direction[0]].designateMountNeighbor()

    return nodeMap

# Retriever for the f value sorting
def getHeuristic(node):
    return node.getFValue()

def graphsearch(map, flag, procedure_name):

    timer= timeit.timeit()

    nodeMap, start, goal= processMap(map)

    directions= [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

    nodeMap= markMountain(nodeMap, directions)

    open= []
    closed= []

    # If A algorithm find heuristic for all nodes (Diagonal Distance Heuristic Function)
    if procedure_name == "A":
        goalX= goal.getCoordinate()[0]
        goalY = goal.getCoordinate()[1]
        d2 = 1
        d = 2
        for row in nodeMap:
            for node in row:
                nodeCoor= node.getCoordinate()
                dx= abs(nodeCoor[0] - goalX)
                dy = abs(nodeCoor[1] - goalY)
                hValue= (d*(dx+dy)) + ((d2-(2*d)) * min(dx,dy))
                node.setHeuristic(hValue)

    # Start initialization
    idNumber= 0

    start.setOperator('S')
    start.setIdentifier('N'+str(idNumber))

    open.append(start)

    solution = "S-R-RD-D-D-LD-G"

    # While the open is not empty
    while len(open) > 0:
        mContainer= []
        # Get a new node from current
        current= open.pop()

        # If goal is reached print result
        if current == goal:

            point= current
            solution= ' G'

            while point is not None:
                solution+= '-' + point.getOperator()
                point= point.getParent()

            solution= solution[::-1]
            print("The program takes ", timer, 'seconds')
            return  solution + str(goal.getActual())

        # Detect duplicate, if duplicate continue
        if current.isClosed():
            continue

        if procedure_name == "D":
            bound = 15  # you have to determine its value
            mContainer, idNumber= expandNode(nodeMap, current, closed, directions, idNumber, bound)
            open.extend(mContainer[::-1])

        elif procedure_name == "A":
            bound = -1  # -1 for A
            mContainer, idNumber= expandNode(nodeMap, current, closed, directions, idNumber, bound)
            open.extend(mContainer)
            open.sort(key= getHeuristic, reverse= True)
        else:
            print("invalid procedure name")
            return "invalid procedure name"

        # run diagnostic
        if flag >= 1:
            flag-= 1
            diagnostic(current, open, closed)

    print("The program takes ",timer, 'seconds')
    return "NO-PATH"

def diagnostic(current, open, closed):

    # Get the first line

    cleanOpen= []
    orderEx= 1

    # create open with no duplicates
    for node in reversed(open):
        if not node.duplicated:
            cleanOpen.append(node)
            node.setExpansion(orderEx)
            orderEx+= 1


    print(backtrack(current), str(current.getOperator()), str(current.getExpansion()), str(current.getActual()), str(current.getHValue()), str(current.getFValue()))

    # Get the 2nd Line

    print("Children: {", end="")
    for child in current.getChildrens():
        print('(' + backtrack(child), child.getOperator(), end='), ')
    print("}")

    # Get the 3rd Line
    print("OPEN: {", end='')
    for node in cleanOpen:
        print('(' + backtrack(node), node.getOperator(), str(node.getActual()), str(node.getHValue()), str(node.getFValue()), end='), ')
    print("}")

    # Get the 4th Line
    print("CLOSED: {", end='')
    for node in closed:
        print('(' + backtrack(node), node.getOperator(), str(node.getExpansion()), str(node.getActual()), str(node.getHValue()), str(current.getFValue()), end='), ')
    print("}")

    for node in open:
        node.setDuplicate(False)

    print()

# Find path from start to here
def backtrack(node):
    # Backtrack to find the path from start to current
    pointer = node
    path = ''

    while pointer.getParent() is not None:
        path += pointer.getOperator() + '-'
        pointer = pointer.getParent()
    path+= pointer.getOperator()

    path= path[::-1]

    return node.getIdentifier() + ':' + path


def read_from_file(file_name):
    # You can change the file reading function to suit the way
    # you want to parse the file
    file_handle = open(file_name)
    map = file_handle.readlines()

    return map


###############################################################################
########### DO NOT CHANGE ANYTHING BELOW ######################################
###############################################################################

def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')
    file_handle.write(solution)

def main():
    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)
    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)
    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)
    parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)


    # get all the arguments
    arguments = parser.parse_args()

##############################################################################
# these print statements are here to check if the arguments are correct.
#    print("The input_file_name is " + arguments.input_file_name)
#    print("The output_file_name is " + arguments.output_file_name)
#    print("The flag is " + str(arguments.flag))
#    print("The procedure_name is " + arguments.procedure_name)
##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":
        input_file_name = arguments.input_file_name
        input_tokens = input_file_name.split("\\")
        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")
            return -1

        output_file_name = arguments.output_file_name
        output_tokens = output_file_name.split("\\")
        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")
            return -1
    else:
        input_file_name = arguments.input_file_name
        input_tokens = input_file_name.split("/")
        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")
            return -1

        output_file_name = arguments.output_file_name
        output_tokens = output_file_name.split("/")
        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")
            return -1

    flag = arguments.flag
    procedure_name = arguments.procedure_name


    try:
        map = read_from_file(input_file_name) # get the map
    except FileNotFoundError:
        print("input file is not present")
        return -1
    # print(map)
    solution_string = "" # contains solution
    write_flag = 0 # to control access to output file

    # take a decision based upon the procedure name
    if procedure_name == "D" or procedure_name == "A":
        solution_string = graphsearch(map, flag, procedure_name)
        write_flag = 1
    else:
        print("invalid procedure name")

    # call function write to file only in case we have a solution
    if write_flag == 1:
        write_to_file(output_file_name, solution_string)

if __name__ == "__main__":
    main()