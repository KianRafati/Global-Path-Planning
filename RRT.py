import math
import time
import pygame
from RRTbasePy import Node, RRTGraph
from RRTbasePy import RRTMap


def main():
    dimensions = (600, 1000)
    start = (150, 50)
    goal = (510, 510)
    obsData = [(500, 20, 100, 30), (100, 200, 80, 60),(400,200,100,200), (800, 300, 40, 170),(200, 400, 100, 150)]
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
                    graph.add_node(randNode)
                    graph.addEdge(TreeNode,randNode)
                    return randNode
            else:
                (px, py) = (randNode.coordinates[0] - TreeNode.coordinates[0],
                                randNode.coordinates[1] - TreeNode.coordinates[1])
                theta = math.atan2(py, px)
                newNode = Node(int(TreeNode.coordinates[0] + Dmax * math.cos(theta)),
                            int(TreeNode.coordinates[1] + Dmax * math.sin(theta)))
                if (graph.isConnectable(TreeNode, newNode)):
                    graph.add_node(newNode)
                    graph.addEdge(TreeNode,newNode)
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
                pygame.draw.circle(map.map, map.grey, node.coordinates, map.nodeRadius)
                pygame.draw.line(map.map, map.grey, node.coordinates, node.parent.coordinates, 1)

    def eraseScreen():
        map.map.fill(map.white)
        map.drawMap(obstacles)

    def parenthood():
        for node in graph.nodes:
            if node.parent is None:
                print('node with id ' + str(graph.getID(node)) + ' has become orphan')
            else:
                print('node with id ' + str(graph.getID(node)) + ' has parent with id ' + str(graph.getID(node.parent)))


    # Insert Nr in graph
    graph.add_node(start)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the user clicked the close button
                running = False  # Set running to False to exit the loop

        max_iterations = 1000  # Set a maximum number of iterations
        iterations = 0

        RRT_Star_DMin = 150

        # RRT* visualization
        while (not graph.isInGraph(Node(*goal))) and (iterations < max_iterations):
            time.sleep(0.1)
            pygame.display.update()
            iterations += 1

            NpNearNnew = []

            # Create Nrand from Xfree
            randNode = graph.randNode()

            # Find Nnear from the tree
            Nnear = graph.findNearRRT(randNode)

            # Expand the tree (length is adjusted by Dmax)
            Nnew = Expand(Nnear, randNode, Dmax=150)

            # Nodes in the tree within Dmin Radius
            Nps = Vicinity(Nnew,RRT_Star_DMin)

            # print('vicinity: '+str(len(Nps)))
            # print('total nodes: '+str(len(graph.nodes)))

            for Np in Nps:
                if graph.cost(Nnew) > graph.cost(Np) + graph.distance(Np,Nnew) and graph.isConnectable(Np,Nnew):
                    graph.removeEdge(Nnew)  # Erase connection to the RRT parent node
                    graph.addEdge(Np,Nnew)  # Setting the Nnearest with RRT*
            
            # Rewiring
            for Np in Nps:
                if graph.cost(Np) > graph.cost(Nnew) + graph.distance(Np,Nnew) and graph.isConnectable(Np,Nnew):
                    graph.removeEdge(Np)
                    graph.addEdge(Nnew,Np)  
                    eraseScreen()

            updateScreen()
            

        if iterations >= max_iterations:
            print("Maximum iterations reached. The goal might be unreachable.")
            break

    pygame.quit()


if __name__ == '__main__':
    main()
