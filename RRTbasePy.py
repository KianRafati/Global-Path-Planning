import random
import math
import traceback
import pygame


class RRTMap:
    def __init__(self, start, goal, MapDimensions, obsData):
        self.start = start
        self.goal = goal
        self.MapDimensions = MapDimensions
        self.MapH, self.MapW = self.MapDimensions

        # window settings
        self.MapWindowName = 'RRT path programming'
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.MapW, self.MapH))
        self.map.fill((255, 255, 255))
        self.nodeRadius = 4
        self.nodeThickness = 0
        self.edgeThickness = 1

        self.obstacles = []
        self.obsData = obsData

        # Colors
        self.grey = (70, 70, 70)
        self.Blue = (0, 0, 255)
        self.Green = (0, 255, 0)
        self.Red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.Black = (0, 0, 0)

    def drawMap(self, obstacles):
        pygame.draw.circle(self.map, self.Green, self.start,
                           self.nodeRadius + 5, 0)
        pygame.draw.circle(self.map, self.Red, self.goal,
                           self.nodeRadius + 5, 0)
        self.drawObs(obstacles)

    def drawPath(self):
        pass

    def drawObs(self, obstacles):
        obstaclesList = obstacles.copy()
        while (len(obstaclesList) > 0):
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(self.map, self.grey, obstacle)


class RRTGraph:
    def __init__(self, start, goal, MapDimensions, obsData):
        self.start = Node(*start)
        self.goal = Node(*goal)
        self.goalFlag = False
        self.MapH, self.MapW = MapDimensions

        # initialize the tree
        self.nodes = [Node(*start)]

        # initialize the obstacles
        self.obstacles = []
        self.obsData = obsData

        # initialize the path
        self.goalState = None
        self.path = []

    def number_of_nodes(self):
        return len(self.nodes)

    def makeObs(self):
        obs = []
        for (x, y, width, height) in self.obsData:
            rectang = None
            Collides = True
            while Collides:
                rectang = pygame.Rect(x, y, width, height)
                if rectang.collidepoint(self.start.coordinates) or rectang.collidepoint(self.goal.coordinates):
                    Collides = True
                else:
                    Collides = False
            obs.append(rectang)
        self.obstacles = obs.copy()
        return obs

    def add_node(self, node):
        if isinstance(node, Node):
            self.nodes.append(node)

    def remove_node(self, node):
        for i in range(0, self.number_of_nodes()):
            if (self.nodes[i].isEqual(node)):
                self.nodes.pop[i]
                return

    def addEdge(self, parent, child):
        if isinstance(child, Node) and hasattr(child, 'setParent') and callable(child.setParent):
            child.setParent(parent)

    def removeEdge(self, child):
        if isinstance(child, Node) and hasattr(child, 'setParent') and callable(child.setParent):
            child.setParent(None)

    def distance(self, node1, node2):
        if isinstance(node1, Node) and isinstance(node2, Node):
            (x1, y1) = node1.coordinates
            (x2, y2) = node2.coordinates
            squared_distance = (float(x1) - float(x2))**2 + \
                (float(y1) - float(y2))**2
            return squared_distance**0.5
        return float('inf')

    def sample_env(self):
        x = int(random.uniform(0, self.MapW))
        y = int(random.uniform(0, self.MapH))
        return x, y

    def randNode(self):
        while True:
            node = Node(*self.sample_env())
            if self.isFree(node):
                break
        return node

    def isFree(self, node):
        if isinstance(node, Node):
            (x, y) = node.coordinates
            obs = self.obstacles.copy()
            while len(obs) > 0:
                rectang = obs.pop(0)
                if rectang.collidepoint(x, y):
                    return False
            return True

    import pygame


    def crossObstacle(self, x1, x2, y1, y2, MWD):
        obs = self.obstacles.copy()
        while len(obs) > 0:
            rectang = obs.pop(0)

            # Inflate the obstacle's dimensions by MWD
            inflated_rect = rectang.inflate(MWD, MWD)

            for i in range(0, 101):
                u = i / 100
                x = x1 * u + x2 * (1 - u)
                y = y1 * u + y2 * (1 - u)

                # Check if the line intersects with the inflated obstacle
                if inflated_rect.collidepoint(x, y):
                    return True

        return False

    # this function connects the new nodes to the tree

    def connect(self, node1, node2):
        if isinstance(node1, Node) and isinstance(node2, Node):
            (x1, y1) = node1.coordinates
            (x2, y2) = node2.coordinates
            if self.crossObstacle(x1, x2, y1, y2):
                self.remove_node(node2)
                return False
            else:
                self.add_node(node2)
                self.addEdge(node1, node2)
                return True

    def isConnectable(self, node1, node2,MWD):
        if isinstance(node1, Node) and isinstance(node2, Node):
            (x1, y1) = node1.coordinates
            (x2, y2) = node2.coordinates
            if self.crossObstacle(x1, x2, y1, y2,MWD):
                return False
            else:
                return True

    def nearest(self, n):
        dmin = self.distance(0, n)
        nnear = 0
        for i in range(0, n):
            if self.distance(i, n) < dmin:
                dmin = self.distance(i, n)
                nnear = i
        return nnear

    def isInGraph(self, node):
        if isinstance(node, Node):
            for nodeI in self.nodes:
                if (node.isEqual(nodeI)):
                    return True
            return False

    def findNearRRT(self, node):
        if isinstance(node, Node):
            Nnear = None
            minDis = float('inf')
            for nodeI in self.nodes:
                if (minDis >= self.distance(nodeI, node)):
                    minDis = self.distance(nodeI, node)
                    Nnear = nodeI
            return Nnear

    def getID(self, node):
        # print(node[0])
        # print(node[1])
        counter = 0
        for nodeI in self.nodes:
            counter += 1
            if (nodeI.isEqual(node)):
                return counter
        traceback.print_stack()
        return 0

    def cost(self, node):
        if isinstance(node, Node):
            if node.parent is None:
                return 0
            return self.distance(node, node.parent) + self.cost(node.parent)

    def findNearRRTstar(self, node, RRT_Star_DMin):
        Nnearest = None
        minCost = float('inf')  # Initialize minCost as positive infinity
        for other_node in self.nodes:
            if self.distance(other_node, node) <= RRT_Star_DMin:
                total_cost = self.cost(other_node) + \
                    self.distance(other_node, node)
                if minCost > total_cost:
                    Nnearest = other_node
                    minCost = total_cost
        return Nnearest


class Node:
    def __init__(self, x, y):
        self.coordinates = (x, y)
        self.parent = None

    def isEqual(self, other_node):
        if isinstance(other_node, Node):
            return self.coordinates == other_node.coordinates

    def setParent(self, parent):
        self.parent = parent
