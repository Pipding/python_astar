from graphics import *
import math
from typing import List

class vector2():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

class gridNodePathfindingStruct():
    def __init__(self, parent=None, nodeIndex=None):
        self.parent = parent
        self.nodeIndex = nodeIndex

        self.f = 0
        self.g = 0
        self.h = 0

        def __eq__(self, other):
            return self.nodeIndex == other.nodeIndex

class gridNodeEdge():
    def __init__(self, nodeIndex=None, otherNodeIndex=None, cost=1):
        self.nodeIndex = nodeIndex
        self.otherNodeIndex = otherNodeIndex
        self.cost = cost

windowWidth = 800
windowHeight = 600

gridWidth = 10
gridHeight = 10

startNode = vector2(0, 0)
endNode = vector2(9, 9)

# Declare the parallel arrays that will represent the grid
gridNodes                                                       =    [0] * (gridHeight * gridWidth)
gridNodePathfindingStructs:List[gridNodePathfindingStruct]      =    []
gridNodeEdges                                                   =    [list[gridNodeEdge]([]) for _ in range(gridHeight * gridWidth)] # Nested list

def isIndexOnEasternEdge(index):
    return ((index % gridWidth) == (gridWidth - 1))

def isIndexOnWesternEdge(index):
    return ((index % gridWidth) == 0)

def isIndexOnNorthernEdge(index):
    return ((index + gridWidth) >= len(gridNodes))

def isIndexOnSouthernEdge(index):
    return ((index - gridWidth) < 0)

# Initialize gridNodes
for x in range(gridHeight * gridWidth):
    gridNodes[x] = x

# Initialize gridNodePathfindingStructs
for node in gridNodes:
    gridNodePathfindingStructs.append(gridNodePathfindingStruct(None, node))

# Initialize gridNodeEdges
for node in gridNodes:
    if(not isIndexOnEasternEdge(node)):
        gridNodeEdges[node].append(gridNodeEdge(node, node + 1, 1))

        if(not isIndexOnNorthernEdge(node)):
            gridNodeEdges[node].append(gridNodeEdge(node, node + gridWidth + 1, 1.4))

        if(not isIndexOnSouthernEdge(node)):
            gridNodeEdges[node].append(gridNodeEdge(node, (node - gridWidth) + 1, 1.4))

    if(not isIndexOnWesternEdge(node)):
        gridNodeEdges[node].append(gridNodeEdge(node, node - 1, 1))

        if(not isIndexOnNorthernEdge(node)):
            gridNodeEdges[node].append(gridNodeEdge(node, (node + gridWidth) - 1, 1.4))

        if(not isIndexOnSouthernEdge(node)):
            gridNodeEdges[node].append(gridNodeEdge(node, (node - gridWidth) - 1, 1.4))

    if(not isIndexOnNorthernEdge(node)):
        gridNodeEdges[node].append(gridNodeEdge(node, node + gridWidth, 1))

    if(not isIndexOnSouthernEdge(node)):
        gridNodeEdges[node].append(gridNodeEdge(node, node - gridWidth, 1))

window = GraphWin('Map', (windowWidth / gridWidth) * gridWidth, (windowHeight / gridHeight) * gridHeight)

def fillTile(x, y, colour):
    square = Rectangle(Point(x,y), Point(x + 1,y + 1))
    square.draw(window)
    square.setFill(colour)

def getLowestFCost(pathfindingStructList: list[gridNodePathfindingStruct]):
    lowestFcost = pathfindingStructList[0].f
    lowestFcostIndex = pathfindingStructList[0].nodeIndex

    for index, item in enumerate(pathfindingStructList):
        if(item.f < lowestFcost):
            lowestFcost = item.f
            lowestFcostIndex = item.nodeIndex

    return lowestFcostIndex

def indexToCoordinates(index) -> vector2:
    return vector2(index % gridWidth, math.floor(index/gridWidth))

def coordinatesToIndex(coordinates: vector2) -> int:
    if(coordinates.x < gridWidth and coordinates.y < gridHeight):
        return coordinates.x + (coordinates.y * gridWidth)
    else:
        print(f'Invalid coordinates: {coordinates.x}, {coordinates.y}')
        quit()

def isIndexOnEasternEdge(index):
    return ((index % gridWidth) == (gridWidth - 1))

def isIndexOnWesternEdge(index):
    return ((index % gridWidth) == 0)

def isIndexOnNorthernEdge(index):
    return ((index + gridWidth) > len(gridNodes))

def isIndexOnSouthernEdge(index):
    return ((index + gridWidth) < 0)

gridNodeEdges[coordinatesToIndex(vector2(1, 2))].append(gridNodeEdge(coordinatesToIndex(vector2(1, 2)), coordinatesToIndex(vector2(8, 8)), 0))

def astar(origin, destination):
    # Initialize both open and closed list
    open_list = list[gridNodePathfindingStruct]([])
    closed_list = []

    open_list.append(gridNodePathfindingStructs[origin])
    current_node = open_list[0]

    # Loop until destination is found or we run out of open nodes
    while len(open_list) > 0:
        
        current_node = getLowestFCost(open_list)
        open_list.remove(gridNodePathfindingStructs[current_node])
        closed_list.append(current_node)

        if(current_node == destination):
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = gridNodePathfindingStructs[current].parent
            return path[::-1] # Return reversed path

        for index, edge in enumerate(gridNodeEdges[current_node]):
            if edge.otherNodeIndex in closed_list:
                next
            else:
                gridNodePathfindingStructs[edge.otherNodeIndex].g = gridNodePathfindingStructs[edge.nodeIndex].g + edge.cost
                gridNodePathfindingStructs[edge.otherNodeIndex].h = indexToCoordinates(edge.otherNodeIndex).distance(indexToCoordinates(destination))
                gridNodePathfindingStructs[edge.otherNodeIndex].f = gridNodePathfindingStructs[edge.otherNodeIndex].g + gridNodePathfindingStructs[edge.otherNodeIndex].h

                if(gridNodePathfindingStructs[edge.otherNodeIndex] in open_list):
                    if(gridNodePathfindingStructs[edge.otherNodeIndex].g > gridNodePathfindingStructs[current_node].g):
                        next
                else:
                    open_list.append(gridNodePathfindingStructs[edge.otherNodeIndex])
                    gridNodePathfindingStructs[edge.otherNodeIndex].parent = current_node

def main():
    # Grid & window setup
    window.setCoords(0.0, 0.0, gridWidth, gridHeight)
    window.setBackground("white")

    for x in range(gridWidth):
        line = Line(Point(x, 0), Point(x, gridHeight * (windowHeight / gridHeight)))
        line.draw(window)
    
    for y in range(gridHeight):
        line = Line(Point(0, y), Point(gridWidth * (windowWidth / gridWidth), y))
        line.draw(window)

    # Determine and draw path
    path = astar(coordinatesToIndex(vector2(0, 0)), coordinatesToIndex(vector2(9, 9)))
    if path == None:
        print("No path available")
    else:
        for nodeindex in path:
            coords = indexToCoordinates(nodeindex)
            fillTile(coords.x, coords.y, "blue")

    window.getMouse()
    window.close()

main()