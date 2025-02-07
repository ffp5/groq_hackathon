import pygame
from agent import VillageAgent
from map import GameMap

def main():
    pygame.init()
    pygame.font.init()  # ensure the font module is initialized
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    game_map = GameMap()
    agents = [
        VillageAgent("Villager1", (50, 240)),   # start on the left side
        VillageAgent("Villager2", (590, 240))   # start on the right side
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update agents
        for agent in agents:
            agent.update(agents)

        screen.fill((0, 0, 0))
        game_map.render(screen)
        for agent in agents:
            agent.render(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
