import pygame
import random
from grock_api_1 import generate_dialogue1  # corrected import
from grock_api_2 import generate_dialogue2  # corrected import
import math

class VillageAgent:
    def __init__(self, name, pos):
        self.name = name
        self.pos = list(pos)
        self.radius = 32  # increased from 16 to 32
        self.color = (255, 255, 255)
        self.dialogue = ""
        self.font = pygame.font.SysFont("Comic Sans MS", 14)  # Changed font to be more comic-like
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]  # new velocity attribute
        self.convo_timer = 0  # new conversation cooldown in frames
        self.bounce_timer = 0
        self.spin = 0
        self.emote_timer = 0
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
        # Add funny movements
        if random.random() < 0.01:  # 1% chance per frame
            self.bounce_timer = 30
            self.spin = random.choice([-10, 10])
        
        if self.bounce_timer > 0:
            self.bounce_timer -= 1
            self.pos[1] += math.sin(self.bounce_timer * 0.2) * 2

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

    def draw_speech_bubble(self, screen, text, pos_x, pos_y):
        # Calculate text size
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        
        # Bubble parameters
        padding = 10
        bubble_width = text_width + padding * 2
        bubble_height = text_height + padding * 2
        
        # Draw white bubble background
        bubble_rect = pygame.Rect(pos_x - bubble_width//2, pos_y - bubble_height - 20, 
                                bubble_width, bubble_height)
        pygame.draw.ellipse(screen, (255, 255, 255), bubble_rect)
        pygame.draw.ellipse(screen, (0, 0, 0), bubble_rect, 2)  # Black outline
        
        # Draw tail of bubble
        points = [
            (pos_x, pos_y - 20),  # Point towards the speaker
            (pos_x - 10, pos_y - 30),
            (pos_x + 10, pos_y - 30)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), points)
        pygame.draw.polygon(screen, (0, 0, 0), points, 2)
        
        # Draw text
        screen.blit(text_surface, 
                   (pos_x - text_width//2, 
                    pos_y - bubble_height - 20 + padding))

    def render(self, screen):
        # Draw the agent using its circular image if available
        if self.image:
            if self.bounce_timer > 0:
                # Rotate image when bouncing
                rotated = pygame.transform.rotate(self.image, self.spin * (self.bounce_timer/30))
                screen.blit(rotated, (self.pos[0] - self.radius, self.pos[1] - self.radius))
            else:
                screen.blit(self.image, (self.pos[0] - self.radius, self.pos[1] - self.radius))
        else:
            pygame.draw.circle(screen, self.color, self.pos, self.radius)

        # Draw speech bubble if there's dialogue
        if self.dialogue:
            # Add emojis to dialogue randomly
            emojis = ["😄", "❤️", "✨", "🌟", "😎"]
            if random.random() < 0.1:  # 10% chance per frame
                self.dialogue += f" {random.choice(emojis)}"
            
            self.draw_speech_bubble(screen, self.dialogue, 
                                  self.pos[0], self.pos[1] - self.radius)
