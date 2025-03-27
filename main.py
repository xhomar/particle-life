import pygame
import sys
import numpy as np
from random import randint


pygame.init()

pygame.display.set_caption("Particle Life")

SCREEN = pygame.display.set_mode((1280, 720))
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = pygame.display.get_window_size()
SIMULATION = pygame.Surface((128, 72))
SIMULATION_WIDTH, SIMULATION_HEIGHT = SIMULATION_SIZE = SIMULATION.get_size()
CLOCK = pygame.Clock()

# particles amount
PARTICLES_GROUPS = 10
PARTICLES_AMOUNT = 1000
PARTICLES_GROUP = int(PARTICLES_AMOUNT / PARTICLES_GROUPS)

# particles groups
particles_position = np.array([np.array([(randint(0, SIMULATION_WIDTH - 1), randint(0, SIMULATION_HEIGHT - 1)) for _ in range(0, PARTICLES_GROUP)]) for _ in range(0, PARTICLES_GROUPS)])
particles_velocity = np.array([np.array([(0, 0) for _ in range(0, PARTICLES_GROUP)]) for _ in range(0, PARTICLES_GROUPS)])
particles_acceleration = np.array([np.array([(0, 0) for _ in range(0, PARTICLES_GROUP)]) for _ in range(0, PARTICLES_GROUPS)])
particles_render = np.array([pygame.Surface((1, 1)) for _ in range(0, PARTICLES_GROUPS)])

# setting color to particles groups
color_range = int(300 / PARTICLES_GROUPS)
color_value = 0
color = pygame.Color(0)
for i in range(0, PARTICLES_GROUPS):
    color.hsla = (color_value, 100, 50, 100)
    particles_render[i].fill((color.r, color.g, color.b, color.a))
    color_value += color_range

print(particles_position)
print(particles_render)

while True:
    # events handling
    for event in pygame.event.get():
        # closes program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key down
        if event.type == pygame.KEYDOWN:
            # randomize particles
            if event.key == pygame.K_r:
                particles_position = np.array([np.array([(randint(0, SIMULATION_WIDTH - 1), randint(0, SIMULATION_HEIGHT - 1)) for _ in range(0, PARTICLES_GROUP)]) for _ in range(0, PARTICLES_GROUPS)])

    # particles render in SIMULATION surface
    SIMULATION.fill((0, 0, 0))
    color = 0
    for particles_group in particles_position:
        for particle in particles_group:
            SIMULATION.blit(particles_render[color], (particle[0], particle[1]))
        color += 1

    # SIMULATION surface rescale and render on SCREEN
    simulation_render = pygame.transform.scale(SIMULATION, SCREEN_SIZE)
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(simulation_render)
    pygame.display.update()
