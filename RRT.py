import math
import time
import pygame
from RRTbasePy import Node, RRTGraph
from RRTbasePy import RRTMap


def main():
    dimensions = (600, 1000)
    start = (150, 50)
    goal = (510, 510)
    obsData = [(500, 20, 100, 30), (100, 200, 80, 60), (300, 300, 40, 70),(200, 120, 100, 200)]
    pygame.init()
    map = RRTMap(start, goal, dimensions, obsData)
    graph = RRTGraph(start, goal, dimensions, obsData)

    obstacles = graph.makeObs()

    map.drawMap(obstacles)

    running = True  # Initialize a variable to control the game loop

    def Expand(TreeNode, randNode, Dmax):
        if isinstance(TreeNode, Node) and isinstance(randNode,Node):
            if (graph.distance(TreeNode, randNode) <= Dmax):
                if (graph.isConnectable(TreeNode, randNode)):
                    (x1, y1) = TreeNode.coordinates
                    (x2, y2) = randNode.coordinates
                    # pygame.draw.line(map.map, map.grey, (x1, y1), (x2, y2))
                    # pygame.draw.circle(map.map, map.Blue, randNode.coordinates, map.nodeRadius)
                    return randNode
            else:
                (px, py) = (randNode.coordinates[0] - TreeNode.coordinates[0],
                                randNode.coordinates[1] - TreeNode.coordinates[1])
                theta = math.atan2(py, px)
                newNode = Node(int(TreeNode.coordinates[0] + Dmax * math.cos(theta)),
                            int(TreeNode.coordinates[1] + Dmax * math.sin(theta)))
                if (graph.isConnectable(TreeNode, newNode)):
                    (x1, y1) = TreeNode.coordinates
                    (x2, y2) = newNode.coordinates
                    # pygame.draw.line(map.map, map.grey, (x1, y1), (x2, y2))
                    # pygame.draw.circle(map.map, map.Blue, newNode.coordinates, map.nodeRadius)
                    return newNode

    # Insert Nr in graph
    graph.add_node(0, start)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the user clicked the close button
                running = False  # Set running to False to exit the loop

        max_iterations = 1000  # Set a maximum number of iterations
        iterations = 0

        RRT_Star_DMin = 150

        # RRT* visualization
        while (not graph.isInGraph(Node(*goal))) and (iterations < max_iterations):
            time.sleep(0.5)
            pygame.display.update()
            iterations += 1

            NpNearNnew = []

            # Create Nrand from Xfree
            randNode = graph.randNode()

            # Find Nnear from the tree
            Nnear = graph.findNearRRT(randNode)

            # Expand the tree (length is adjusted by Dmax)
            Nnew = Expand(Nnear, randNode, Dmax=150)

            # for i in range(0,graph.number_of_nodes()):
            #     NodeI = (graph.x[i],graph.y[i])
            #     if(graph.distance(NodeI,Nnew) < RRT_Star_DMin):
            #         if(graph.Cost(NodeI) > graph.Cost(Nnew) + graph.distance(NodeI,Nnew)):
            #             pass

        if iterations >= max_iterations:
            print("Maximum iterations reached. The goal might be unreachable.")
            break

    pygame.quit()


if __name__ == '__main__':
    main()
