import pygame
import psutil
import platform
from agent import VillageAgent
from map import GameMap

def main():
    pygame.init()
    pygame.font.init()  # ensure the font module is initialized
    screen = pygame.display.set_mode((1024, 768))  # Bigger window
    clock = pygame.time.Clock()

    game_map = GameMap()
    agents = [
        VillageAgent("Villager1", (100, 384)),   # Adjusted starting positions for bigger window
        VillageAgent("Villager2", (924, 384))    # Adjusted starting positions for bigger window
    ]

    # Add system info
    system_info = {
        "OS": platform.system(),
        "CPU Usage": 0,
        "Memory": 0,
        "FPS": 0
    }
    
    debug_font = pygame.font.SysFont("Courier", 16)
    show_debug = True

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
        
        # Update system metrics
        if show_debug:
            system_info["CPU Usage"] = psutil.cpu_percent()
            system_info["Memory"] = psutil.virtual_memory().percent
            system_info["FPS"] = int(clock.get_fps())
            
            # Draw system info
            y_pos = 10
            for key, value in system_info.items():
                text = f"{key}: {value}"
                surface = debug_font.render(text, True, (255, 255, 0))
                screen.blit(surface, (screen.get_width() - 200, y_pos))
                y_pos += 25

        # Add keyboard controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:  # Toggle debug info
            show_debug = not show_debug
        if keys[pygame.K_r]:  # Reset metrics
            for agent in agents:
                agent.metrics = {
                    "response_times": [],
                    "interaction_count": 0,
                    "avg_distance": [],
                    "mood": "neutral"
                }

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
