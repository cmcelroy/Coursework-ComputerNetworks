#########################################################################################################################
###
###      Name: Chris McElroy
###      Date: 11-13-20
###     Class: CSC450
###   Summary: Project - This program reads CSV files, processes the data into nodes and link cost.
###                      The program uses Dijkstra's algorithm to compute the shortest path and least-cost paths in the network.
###                      The program uses Bellman-Ford equation to calculate distance vectors for each node.
###
###   To Run: python routing.py <"CSV File">
###
###   Sample: python routing.py topology-1.csv
###
#########################################################################################################################


import sys
import csv

### Globals ###
# nodes
NODES = []  
# edge cost
EDGE_COST = {}
# node graph
NODE_GRAPH = {}
# list to maintain updated values
UPDATED_VALUES = {}

# declare infinity
inf = 99999

# Dijkstras algorithm
def dijkstras(startNode):
    
    global NODES
    global EDGE_COST

    cost = {}
    stopPoints = {}
    addedCost = 0
    
    # loop builds a list a cost and each stop point in the list
    for i in range(0, len(NODES)):
        cost[NODES[i]] = 9999
        stopPoints[NODES[i]] = False

    # set starting node and maintain visisted node for later use
    currentNode = startNode
    nextNode = currentNode
    cost[currentNode] = [0, currentNode]

    # work through network until complete
    while(1):
        # set minimum path to max
        minPath = 9999      
        # set current node visited true
        stopPoints[currentNode] = True     

        # checks item in list generated, then against currentNode, then connect to node, and cost of link
        for item in EDGE_COST.items():
            # set previous weight to max
            prevCost = 9999
            edgeLabel = item[0]
            # check if the node the edge is connected to is visited and that the start of the edge is the current node
            if((edgeLabel[0] == currentNode) and (stopPoints[edgeLabel[1]] == False)):    
                # set a temporary cost for link to specified current node plus the edge
                tempCost = int(item[1]) + addedCost     
                # get the end nodes name
                endNode = edgeLabel[1]    
                # get the end node data
                nodeInfo = cost[endNode[0]]
                # assign value to previous cost
                if (nodeInfo == 9999):
                    prevCost = nodeInfo
                else:
                    prevCost = nodeInfo[0]

                if(tempCost < prevCost):
                    cost[edgeLabel[1]] = [tempCost, edgeLabel[0]]
        
        # determines next node to travel to
        for item in cost.items():
            # checks for untouched node
            if(item[1] != 9999):
                if (int(item[1][0]) < minPath and stopPoints[item[0]] == False):
                    minPath = int(item[1][0])
                    nextNode = item[0]
        # ...if nextNode is equal to currentNode then finished
        if (nextNode == currentNode):
            return cost
        # if not, travel to next node and add cost
        else:
            currentNode = nextNode
            newInfo = cost[currentNode]
            addedCost = newInfo[0]

# Distance Vector 
def distVect():
    # create a node graph
    for node in NODES:
        new_dict = {}
        for key in EDGE_COST.keys():
            if(node in key[0]):
                new_dict[key] = EDGE_COST[key]
                UPDATED_VALUES[key] = EDGE_COST[key]
            else:
                new_dict[key] = inf
        NODE_GRAPH[node] = new_dict

    while(UPDATED_VALUES):
        # update node with new cost
        for key in UPDATED_VALUES.keys():
            for node in NODES:
                if(key[0] != node):
                    NODE_GRAPH[node][key] = UPDATED_VALUES[key]
        UPDATED_VALUES.clear()
        for checkNode in NODES:
            for endNode in NODES:
                # find the minimum distance vector
                minDist = inf
                for interNode in NODES:
                    if(minDist > NODE_GRAPH[checkNode][checkNode+interNode]+NODE_GRAPH[checkNode][interNode+endNode]):
                        minDist = NODE_GRAPH[checkNode][checkNode+interNode]+NODE_GRAPH[checkNode][interNode+endNode]
                #updates min. distance vector
                if(minDist < NODE_GRAPH [checkNode][checkNode+endNode]):
                    NODE_GRAPH[checkNode][checkNode+endNode] = minDist
                    UPDATED_VALUES[checkNode+endNode] = minDist
    # print out distance vectors
    for node in NODE_GRAPH:
        printLine = "Distance vector for node {}:".format(node)
        pathList = NODE_GRAPH.get(str(node))
        pathListNodes = []
        newCostsList = []
        for path in pathList:
            pathListNodes.append(path)
        # sort node list
        pathListNodes.sort()
        # sorted new list
        for i in range(0, len(pathListNodes)):
            newCostsList.append(pathListNodes[i])
            newCostsList.append(pathList.get(pathListNodes[i]))
        # print out
        for i in range(0, int(len(newCostsList)/2)):
            pathName = newCostsList[i*2]           
            if (pathName[0] == node):
                printLine = printLine + " " + str(newCostsList[i*2+1])
        print(printLine)

# Input CSV file
def csvInput(csvFile):
    
    global NODES
    global NODE_COST
    
    # input of rows from file
    inputData = []
    temp = {}
    
    # parses data from CSV
    with open(csvFile, 'rt') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            inputData.append(row)
        # retreive nodes
        NODES = inputData[0][1:len(inputData[0])]
        # retrieves column data
        for i in range(1, len(inputData[0])):
            for j in range(i,len(inputData[0])):
                # builds cost and nodes into reference
                edgeLabel = str(inputData[0][i] + inputData[0][j])
                edgeCost = int(inputData[i][j])
                EDGE_COST[edgeLabel] = edgeCost
                temp[edgeLabel] = edgeCost

        for i in temp:
            if(i[0] != i[1]):
                EDGE_COST[str(i[1]+i[0])] = EDGE_COST[i]
                

# Select starting node
def chooseNode():
    finalNode = 0
    # allow user to select an acceptable node
    while(1):
        try:
            node = str(input("\nPlease, select a node: "))
            print("------------------------------------------------")
        except ValueError:
            node = ""
        # check listed nodes to verify selected node is in the list
        for i in range(0, len(NODES)):
            if(node == NODES[i]):
                finalNode = node
                return finalNode

### MAIN ###
def main():
    nodeSelection = ''
    csvFile = str(sys.argv[1])
    csvInput(csvFile)
    # Pulls in the node you want
    nodeChoice = chooseNode()
    # gets the dictionary of paths from dijkstras
    paths = dijkstras(nodeChoice)

    # processes input from dijkstras algorithm
    created = {}
    for item in paths.items():
        created[item[0]] = False
    # path ordered
    pathOrder = {}
    
    for i in range(0, len(paths)*len(paths)):
        # receives paths
        for item in paths.items():
            
            if(item[0] == nodeSelection):
                pathOrder[nodeSelection] = nodeSelection
                created[nodeSelection] = True
            else:
                prevNode = item[1][1]
                if(created[prevNode] and not(created[item[0]])):
                    created[item[0]] = True
                    pathOrder[item[0]] = pathOrder[prevNode] + item[0]
    
    # print the shortest path
    outputPrintTrees = "Shortest path tree for node {}:\n".format(nodeSelection)
    for item in pathOrder.items():
        if(item[0] != nodeSelection):
            outputPrintTrees = outputPrintTrees + item[1] + ", "
    print(outputPrintTrees)
    
    # print the least costs path
    outputPrintPaths = "Costs of least-cost paths for node {}:\n".format(nodeSelection)
    for item in paths.items():
        outputPrintPaths = outputPrintPaths + item[0] + ":" + str(item[1][0]) + ", "
    print(outputPrintPaths)
    print("------------------------------------------------")


main()
distVect()
print("\n")
