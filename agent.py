import pygame
import random
from grock_api_1 import generate_dialogue1  # corrected import
from grock_api_2 import generate_dialogue2  # corrected import
import math
import time
from statistics import mean

# Add Particle class at the top of the file
class Particle:
    def __init__(self, x, y, particle_type):
        self.x = x
        self.y = y
        self.type = particle_type  # 'heart' or 'thunder'
        self.lifetime = 60  # frames
        self.scale = random.uniform(0.5, 1.5)
        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-2, -1)  # Move upward

    def update(self):
        self.lifetime -= 1
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # gravity effect

    def render(self, screen):
        alpha = int((self.lifetime / 60) * 255)
        if self.type == 'heart':
            color = (255, 192, 203, alpha)  # pink
            size = int(10 * self.scale)
            pos = (int(self.x), int(self.y))
            pygame.draw.circle(screen, color, (pos[0] - size//4, pos[1]), size//2)
            pygame.draw.circle(screen, color, (pos[0] + size//4, pos[1]), size//2)
            points = [
                (pos[0], pos[1] + size//2),
                (pos[0] - size//2, pos[1] - size//4),
                (pos[0] + size//2, pos[1] - size//4),
            ]
            pygame.draw.polygon(screen, color, points)
        elif self.type == 'thunder':
            color = (255, 255, 0, alpha)  # yellow
            points = [
                (self.x, self.y),
                (self.x - 5 * self.scale, self.y + 10 * self.scale),
                (self.x + 2 * self.scale, self.y + 8 * self.scale),
                (self.x - 2 * self.scale, self.y + 15 * self.scale),
            ]
            pygame.draw.polygon(screen, color, points)

class VillageAgent:
    def __init__(self, name, pos):
        self.name = name
        self.pos = list(pos)
        self.radius = 48  # Increased from 32 to 48 for bigger agents
        self.color = (255, 255, 255)
        self.dialogue = ""
        self.font = pygame.font.SysFont("Comic Sans MS", 20)  # Bigger font
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]  # new velocity attribute
        self.convo_timer = 0  # new conversation cooldown in frames
        self.bounce_timer = 0
        self.spin = 0
        self.emote_timer = 0
        self.particles = []  # Add this line
        self.metrics = {
            "response_times": [],
            "interaction_count": 0,
            "avg_distance": [],
            "mood": "neutral"
        }
        self.debug_info = True  # Toggle for technical overlay
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
        start_time = time.time()
        # Update existing particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

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
        if self.pos[0] < 0 or self.pos[0] > 1024:
            self.vel[0] *= -1
        if self.pos[1] < 0 or self.pos[1] > 768:
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
                    distance = pygame.math.Vector2(self.pos).distance_to(agent.pos)
                    self.metrics["avg_distance"].append(distance)
                    if distance < 50 and self.convo_timer == 0:
                        self.metrics["interaction_count"] += 1
                        response_time = time.time() - start_time
                        self.metrics["response_times"].append(response_time)
                        dialogue1 = generate_dialogue1("Villager1", "Villager2", "")
                        dialogue2 = generate_dialogue2("Villager2", "Villager1", "")
                        self.dialogue = dialogue1
                        agent.dialogue = dialogue2
                        # Print the conversation to the terminal
                        print("=== Conversation ===")
                        print(f"Villager1 (Woman): {dialogue1}")
                        print(f"Villager2 (Man): {dialogue2}")
                        print("====================")
                        print("""Riley: Ugh, don’t think I haven’t noticed you’re secretly admiring me again.
Jordan: Admiring? Me? I’m just noticing you’re out here doing your thing… as usual.
Riley: Oh, please. That “thing” of yours isn’t that spectacular. I’m the main attraction, remember?
Jordan: Main attraction? I’d say you’re more like the bonus feature—unexpected, but impossible to ignore.
Riley: Bonus feature, huh? So you’re saying you’d be lost without my dazzling commentary on your life?
Jordan: Lost? Hardly. I’m perfectly capable of navigating without you. But, then again, even GPS systems enjoy a little sass from time to time.
Riley: Ha! If your GPS started quoting my one-liners, I’d have to install a “you’re welcome” alert.
Jordan: Keep talking like that, and maybe one day you’ll admit that my “annoying” charm is exactly what you secretly need.
Riley: Secretly need? Don’t flatter yourself. I’m just here, tolerating your relentless “wit” because it makes my day less boring.
Jordan: Tolerating? That word must be mispronounced by you. I prefer “appreciating”—even if you insist on calling it toleration.
Riley: Appreciating, tolerating, whatever. You know what, if I had to choose between a day without your snark and a day without my own brilliance, I’d pick my brilliance every time.
Jordan: Sure, because brilliance isn’t accompanied by a certain soft spot for my every “accidental” compliment.
Riley: Accidental compliments? Look, I don’t do compliments. I just state facts, and the fact is, you’re dangerously good at being adorable.
Jordan: Adorable? Don’t make me blush. Blushing might just give you the courage to admit that you care.
Riley: I care about you, obviously—if only I could package it in a way that sounds less like a sappy love note and more like a cleverly delivered insult.
Jordan: Oh, so you care? That’s shocking coming from someone who claims not to.
Riley: Shocking? Please. I care about you too—just don’t expect me to announce it like I’m handing out medals at a parade.
Jordan: Fine. Our secret “non-relationship” remains our little charade, then.
Riley: Exactly. Now, how about we grab coffee and continue our battle of wits?
Jordan: Only if you’re buying. After all, I wouldn’t want my “bonus feature” to run out of fuel.
Riley: Fuel’s on me, hotshot. And remember: if you ever slip and admit you’re falling for me, I’ll be right here, ready to roll my eyes in the most endearing way possible.
Jordan: Endearing? That’s a dangerous word coming from you—but fine, let’s roll.
Riley: May the sass be with us, then.
Jordan: Always.""")
                        self.convo_timer = 120  # set cooldown (e.g., 120 frames)
                        agent.convo_timer = 120
                    elif pygame.math.Vector2(self.pos).distance_to(agent.pos) >= 50:
                        self.dialogue = ""
                        agent.dialogue = ""
                    # Add particles when agents are close
                    if pygame.math.Vector2(self.pos).distance_to(agent.pos) < 50:
                        if random.random() < 0.1:  # 10% chance per frame
                            mid_x = (self.pos[0] + agent.pos[0]) / 2
                            mid_y = (self.pos[1] + agent.pos[1]) / 2
                            particle_type = random.choice(['heart', 'thunder'])
                            self.particles.append(Particle(mid_x, mid_y, particle_type))

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
        
        # Render particles
        for particle in self.particles:
            particle.render(screen)
        
        # Add technical overlay
        if self.debug_info:
            metrics_font = pygame.font.SysFont("Courier", 14)
            y_offset = 10
            metrics_text = [
                f"Agent: {self.name}",
                f"Interactions: {self.metrics['interaction_count']}",
                f"Avg Response: {mean(self.metrics['response_times']) if self.metrics['response_times'] else 0:.3f}s",
                f"Avg Distance: {mean(self.metrics['avg_distance']) if self.metrics['avg_distance'] else 0:.1f}px",
                f"FPS: {int(clock.get_fps())}"
            ]
            
            for text in metrics_text:
                surface = metrics_font.render(text, True, (255, 255, 0))
                screen.blit(surface, (10, y_offset))
                y_offset += 20
                
            # Draw interaction radius
            pygame.draw.circle(screen, (255, 0, 0), 
                             (int(self.pos[0]), int(self.pos[1])), 
                             50, 1)  # interaction radius visualization
