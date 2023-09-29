import math
import time
import pygame
from RRTbasePy import Node, RRTGraph
from RRTbasePy import RRTMap


def main():
    dimensions = (600, 1000)
    start = (150, 50)
    goal = (710, 110)
    MWD = 50
    Dmax = 150
    #            x , y ,  w  , h
    obsData = [(400, -40, 100, 300),
               (100, 200, 80, 460), 
               (400, 200,100, 200),
               (800, 300, 40, 170),
               (200, 400, 100, 150)]
    pygame.init()
    map = RRTMap(start, goal, dimensions, obsData)
    graph = RRTGraph(start, goal, dimensions, obsData)

    obstacles = graph.makeObs()

    map.drawMap(obstacles)

    running = True  # Initialize a variable to control the game loop
    paused = False  # Initialize a variable to control pause/play state

    def Expand(TreeNode, randNode, Dmax,MWD):
        if isinstance(TreeNode, Node) and isinstance(randNode, Node):
            if (graph.distance(TreeNode, randNode) <= Dmax):
                if (graph.isConnectable(TreeNode, randNode,MWD)):
                    graph.add_node(randNode)
                    graph.addEdge(TreeNode, randNode)
                    return randNode
            else:
                (px, py) = (randNode.coordinates[0] - TreeNode.coordinates[0],
                            randNode.coordinates[1] - TreeNode.coordinates[1])
                theta = math.atan2(py, px)
                newNode = Node(int(TreeNode.coordinates[0] + Dmax * math.cos(theta)),
                               int(TreeNode.coordinates[1] + Dmax * math.sin(theta)))
                if (graph.isConnectable(TreeNode, newNode,MWD)):
                    graph.add_node(newNode)
                    graph.addEdge(TreeNode, newNode)
                    return newNode

    def Vicinity(node, DminRadius):
        if isinstance(node, Node):
            nodeWithinRadius = []
            for Np in graph.nodes:
                if graph.distance(Np, node) <= DminRadius:
                    nodeWithinRadius.append(Np)
            return nodeWithinRadius
        else:
            return []  # Return an empty list if node is not an instance of Node

    def updateScreen():
        for node in graph.nodes:
            if node.parent is not None:
                pygame.draw.circle(map.map, map.grey,
                                   node.coordinates, map.nodeRadius)
                pygame.draw.line(map.map, map.grey,
                                 node.coordinates, node.parent.coordinates, 1)

    def eraseScreen():
        map.map.fill(map.white)
        map.drawMap(obstacles)

    def drawPath(node):
        if isinstance(node,Node) and node.parent is not None:
            pygame.draw.line(map.map,map.Red,node.coordinates,node.parent.coordinates,10)
            drawPath(node.parent)



    startNode = Node(*start)
    goalNode = Node(*goal)

    # Insert Nr in graph
    graph.add_node(startNode)

    max_iterations = 1000  # Set a maximum number of iterations
    iterations = 0
    
    RRT_Star_DMin = 150

    # RRT* visualization
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        time.sleep(0.1)
        pygame.display.update()
        iterations += 1

        # Create Nrand from Xfree
        randNode = graph.randNode()

        # Find Nnear from the tree
        Nnear = graph.findNearRRT(randNode)

        # Expand the tree (length is adjusted by Dmax)
        Nnew = Expand(Nnear, randNode, Dmax,MWD)

        # Nodes in the tree within Dmin Radius
        Nps = Vicinity(Nnew, RRT_Star_DMin)

        for Np in Nps:
            if graph.cost(Nnew) > graph.cost(Np) + graph.distance(Np, Nnew) and graph.isConnectable(Np, Nnew,MWD):
                # Erase connection to the RRT parent node
                graph.removeEdge(Nnew)
                graph.addEdge(Np, Nnew)  # Setting the Nnearest with RRT*
            
        # Rewiring
        for Np in Nps:
            if graph.cost(Np) > graph.cost(Nnew) + graph.distance(Np, Nnew) and graph.isConnectable(Np, Nnew,MWD):
                graph.removeEdge(Np)
                graph.addEdge(Nnew, Np)
                eraseScreen()

        NearGoals = Vicinity(goalNode,DminRadius=200)

        updateScreen()

        # if iterations >= max_iterations:
        #     print("Maximum iterations reached. The goal might be unreachable.")
        #     break

        # Checks to see if we have found a way to the goal or not
        if Vicinity(goalNode,RRT_Star_DMin):
            drawPath(graph.findNearRRT(goalNode))

        

    pygame.quit()


if __name__ == '__main__':
    main()
