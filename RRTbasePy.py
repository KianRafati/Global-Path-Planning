import random
import math
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
        self.nodeRadius = 0
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

    def drawMap(self, obstacles):
        pygame.draw.circle(self.map, self.Green, self.start, self.nodeRadius + 5, 0)
        pygame.draw.circle(self.map, self.Red, self.goal, self.nodeRadius + 5, 0)
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
        (x, y) = start
        self.start = start
        self.goal = goal
        self.goalFlag = False
        self.MapH, self.MapW = MapDimensions
        self.x = []
        self.y = []
        self.parent = []

        # initialize the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        # initialize the obstacles
        self.obstacles = []
        self.obsData = obsData

        # initialize the path
        self.goalState = None
        self.path = []

    def makeObs(self):
        obs = []
        for (x, y, width, height) in self.obsData:
            rectang = None
            Collides = True
            while Collides:
                rectang = pygame.Rect(x, y, width, height)
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    Collides = True
                else:
                    Collides = False
            obs.append(rectang)
        self.obstacles = obs.copy()
        return obs

    def add_node(self):
        pass

    def remove_node(self):
        pass

    def addEdge(self):
        pass

    def removeEdge(self):
        pass
