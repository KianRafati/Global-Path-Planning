import pygame
from RRTbasePy import RRTGraph
from RRTbasePy import RRTMap

def main():
    dimensions = (600, 1000)
    start = (50, 50)
    goal = (510, 510)
    obsData = [(10, 20, 50, 30), (100, 200, 80, 60), (300, 300, 40, 70)]
    pygame.init()
    map = RRTMap(start, goal, dimensions, obsData)
    graph = RRTGraph(start, goal, dimensions, obsData)

    obstacles = graph.makeObs()

    map.drawMap(obstacles)

    pygame.display.update()

    running = True  # Initialize a variable to control the game loop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the user clicked the close button
                running = False  # Set running to False to exit the loop

    pygame.quit()

if __name__ == '__main__':
    main()
