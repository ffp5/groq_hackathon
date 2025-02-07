import pygame

class GameMap:
    def __init__(self):
        # Increase tile size for a more retro, pixelated look
        self.tile_size = 32
        self.tiles = [[(i + j) % 2 for i in range(32)] for j in range(24)]  # More tiles for bigger window

    def render(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                # Use Pokemon-like grassy tones
                color = (106, 190, 48) if tile == 0 else (84, 173, 34)
                rect = (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)
                # Draw a thin border to mimic the grid-style of classic Pokemon games
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
