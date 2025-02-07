import pygame
import random
from grock_api_1 import generate_dialogue1  # corrected import
from grock_api_2 import generate_dialogue2  # corrected import

class VillageAgent:
    def __init__(self, name, pos):
        self.name = name
        self.pos = list(pos)
        self.radius = 32  # increased from 16 to 32
        self.color = (255, 255, 255)
        self.dialogue = ""
        self.font = pygame.font.SysFont("Arial", 12)
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]  # new velocity attribute
        self.convo_timer = 0  # new conversation cooldown in frames
        # Load and process image for agent
        if self.name == "Villager1":
            original_image = pygame.image.load("agent1.jpeg").convert_alpha()
        elif self.name == "Villager2":
            original_image = pygame.image.load("agent2.jpg").convert_alpha()
        else:
            self.image = None
            return

        # Create a circular surface with transparency
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        # Scale the loaded image to fit our desired size
        scaled_image = pygame.transform.scale(original_image, (self.radius * 2, self.radius * 2))
        
        # Create circular mask
        pygame.draw.circle(self.image, (255, 255, 255, 255), (self.radius, self.radius), self.radius)
        
        # Blit the scaled image onto our circular surface
        self.image.blit(scaled_image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    
    def update(self, agents):
        # Natural movement: update velocity with slight random acceleration
        
        self.vel[0] += random.uniform(-0.1, 0.1)
        self.vel[1] += random.uniform(-0.1, 0.1)
        max_speed = 2
        speed = (self.vel[0] ** 2 + self.vel[1] ** 2) ** 0.5
        if speed > max_speed:
            self.vel[0] = (self.vel[0] / speed) * max_speed
            self.vel[1] = (self.vel[1] / speed) * max_speed
        # update position based on velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # boundary checking for a 640x480 window
        if self.pos[0] < 0 or self.pos[0] > 640:
            self.vel[0] *= -1
        if self.pos[1] < 0 or self.pos[1] > 480:
            self.vel[1] *= -1
        
        # Apply seeking behavior towards the other agent
        if self.name in ("Villager1", "Villager2"):
            target = None
            for agent in agents:
                if self.name == "Villager1" and agent.name == "Villager2":
                    target = agent.pos
                elif self.name == "Villager2" and agent.name == "Villager1":
                    target = agent.pos
            if target:
                dx = target[0] - self.pos[0]
                dy = target[1] - self.pos[1]
                distance = (dx**2 + dy**2) ** 0.5
                if distance > 0:
                    # small seeking acceleration coefficient
                    self.vel[0] += (dx/distance) * 0.05
                    self.vel[1] += (dy/distance) * 0.05

        # Decrement conversation timer if active
        if self.convo_timer > 0:
            self.convo_timer -= 1

        # Trigger conversation between Villager1 and Villager2 using different API modules
        if self.name == "Villager1":
            for agent in agents:
                if agent.name == "Villager2":
                    if pygame.math.Vector2(self.pos).distance_to(agent.pos) < 50 and self.convo_timer == 0:
                        dialogue1 = generate_dialogue1("Villager1", "Villager2", "")
                        dialogue2 = generate_dialogue2("Villager2", "Villager1", "")
                        self.dialogue = dialogue1
                        agent.dialogue = dialogue2
                        # Print the conversation to the terminal
                        print("=== Conversation ===")
                        print(f"Villager1 (Woman): {dialogue1}")
                        print(f"Villager2 (Man): {dialogue2}")
                        print("====================")
                        self.convo_timer = 120  # set cooldown (e.g., 120 frames)
                        agent.convo_timer = 120
                    elif pygame.math.Vector2(self.pos).distance_to(agent.pos) >= 50:
                        self.dialogue = ""
                        agent.dialogue = ""

    def render(self, screen):
        # Draw the agent using its circular image if available
        if self.image:
            screen.blit(self.image, (self.pos[0] - self.radius, self.pos[1] - self.radius))
        else:
            pygame.draw.circle(screen, self.color, self.pos, self.radius)
        if self.dialogue:
            text_surface = self.font.render(self.dialogue, True, (255, 255, 0))
            screen.blit(text_surface, (self.pos[0] - 20, self.pos[1] - 30))
