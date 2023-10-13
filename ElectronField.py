import pygame
import math
import random

# Initialize Pygame
pygame.init()
# Set initial conditions

# Define constants
q = 1  # charge (scaled for simplicity)
m = 1  # mass (scaled for simplicity)
e0 = 1  # electric field magnitude
s = 1000 # Time Scale
# Define constants
num_particles = 100 # Number of particles
particle_radius = 2  # Radius of particles
max_speed = 15
#trail_length = 275*math.exp(-0.00177*num_particles)  # Length of the tail
trail_length=40
colormax = 127
# Scaling of the Field
scale_x = 0.0051  # Adjust as needed
scale_y = scale_x  # Adjust as needed

# Get screen information
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Set window size to screen size
window_size = (screen_width, screen_height)

# Define the electric field function
def efield(x, y, t):
    return [math.cos(t - scale_x * x - scale_y * y) + math.cos(t + scale_x * x - scale_y * y), 
            -math.cos(t - scale_x * x - scale_y * y) + math.cos(t + scale_x * x - scale_y * y)]
def generate_grayscale_background(width, height, t):
    background = pygame.Surface((width, height))
    for x in range(width):
        for y in range(height):
            e = efield(x, y, t)
            brightness = int((e[0]**2 + e[1]**2)**0.5 * 255 / (2 * e0))  # Adjust based on your specific formula
            pixel_color = (brightness, brightness, brightness)
            background.set_at((x, y), pixel_color)
    return background

# Define a Particle class
class Particle:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.vel = [0, 0]
        self.trail = []
        self.color = (random.randint(0, colormax), random.randint(0, colormax), random.randint(0, colormax))

    def update(self, t):
        # Calculate acceleration
        e = efield(self.pos[0], self.pos[1], t)
        ax = q / m * e[0]
        ay = q / m * e[1]

        # Update velocity
        self.vel[0] = self.vel[0] + ax
        self.vel[1] = self.vel[1] + ay

        # Update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % window_size[0]
        self.pos[1] = (self.pos[1] + self.vel[1]) % window_size[1]

        # Check speed and set velocities to zero if exceeded max_speed
        speed = self.get_speed()
        if speed > max_speed:
            self.vel = [0,0]

        # Append current position to trail
        self.trail.append((int(self.pos[0]), int(self.pos[1])))

        # Limit the length of the trail
        if len(self.trail) > trail_length:
            self.trail.pop(0)
            
    def get_speed(self):
        return math.sqrt(self.vel[0]**2 + self.vel[1]**2)
    def get_brightness(self):
        # Calculate the brightness based on velocity
        speed = math.sqrt(self.vel[0]**2 + self.vel[1]**2)/s
        brightness = int((speed / max_speed) * 255)
        return min(brightness, 255)  # Ensure brightness is capped at 255
    def draw(self, window):
        brightness = self.get_brightness()
        color = (min(self.color[0] + brightness, 255), 
                 min(self.color[1] + brightness, 255), 
                 min(self.color[2] + brightness, 255))
        pygame.draw.circle(window, color, (int(self.pos[0]), int(self.pos[1])), particle_radius)

        for pos in self.trail:
            pygame.draw.circle(window, color, pos, particle_radius)
# Initialize Pygame window
# Initialize Pygame window
window = pygame.display.set_mode(window_size, pygame.FULLSCREEN)

clock = pygame.time.Clock()

# Create particles
particles = [Particle(random.randint(0, window_size[0]), random.randint(0, window_size[1])) for _ in range(num_particles)]
# Generate grayscale background
#background = generate_grayscale_background(window_size[0], window_size[1], 0)  # Generate once before the main loop

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_SPACE:
                particles = [Particle(random.randint(0, window_size[0]), random.randint(0, window_size[1])) for _ in range(num_particles)]
    if len(particles) <= 0:
        particles = [Particle(random.randint(0, window_size[0]), random.randint(0, window_size[1])) for _ in range(num_particles)]

    t = pygame.time.get_ticks() / s

    # Update particles
    for particle in particles:
        particle.update(t)
        
    # Draw particles
    window.fill((0, 0, 0))
    #window.blit(background, (0, 0))  # Blit the grayscale background (if needed)
    for particle in particles:
        particle.draw(window)
    pygame.display.update()

    clock.tick(120)
