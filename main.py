import pygame
import sys
import numpy as np
from random import randint
from math import e


pygame.init()

pygame.display.set_caption("Particle Life")

SCREEN = pygame.display.set_mode((1280, 720))
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = pygame.display.get_window_size()
SIMULATION = pygame.Surface((128, 72))
SIMULATION_WIDTH, SIMULATION_HEIGHT = SIMULATION_SIZE = SIMULATION.get_size()
CLOCK = pygame.Clock()

# particles forces setups
force_decay = 10

# particles amount
PARTICLES_GROUPS = 2
PARTICLES_AMOUNT = 10
PARTICLES_GROUP = int(PARTICLES_AMOUNT / PARTICLES_GROUPS)

# particles groups
particles_position = np.array([(randint(0, SIMULATION_WIDTH - 1), randint(0, SIMULATION_HEIGHT - 1)) for _ in range(0, PARTICLES_GROUP * PARTICLES_GROUPS)])
particles_velocity = np.zeros(PARTICLES_GROUP * PARTICLES_GROUPS)
particles_acceleration = np.zeros(PARTICLES_GROUP * PARTICLES_GROUPS)
particles_render = np.array([pygame.Surface((1, 1)) for _ in range(0, PARTICLES_GROUPS)])

# interaction matrix
particles_attraction = np.random.randint(-100, 101, (PARTICLES_GROUPS, PARTICLES_GROUP))
print(particles_position)

# setting color to particles groups
color_range = int(300 / PARTICLES_GROUPS)
color_value = 0
color = pygame.Color(0)
for i in range(0, PARTICLES_GROUPS):
    color.hsla = (color_value, 100, 50, 100)
    particles_render[i].fill((color.r, color.g, color.b, color.a))
    color_value += color_range


def accelaration():
    # I hate physics
    distances = 0
    directions = 0
    accelaration = 0
    for particle in particles_position:
        distances = None  # later
        directions = (particle - particles_position)
        acceleration = 0
        for index in range(0, PARTICLES_GROUPS * PARTICLES_GROUP):
            # 1 is particles attraction, to be changed
            acceleration += (1 * e) - ((distances[index] / force_decay) * (directions[index] / distances[index]))


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
                particles_position = np.array([(randint(0, SIMULATION_WIDTH - 1), randint(0, SIMULATION_HEIGHT - 1)) for _ in range(0, PARTICLES_GROUP * PARTICLES_GROUPS)])

    # particles render in SIMULATION surface
    SIMULATION.fill((0, 0, 0))
    for group in range(0, 3):
        for particle in particles_position[group * PARTICLES_GROUP:group * PARTICLES_GROUP + PARTICLES_GROUP]:
            SIMULATION.blit(particles_render[group], (particle[0], particle[1]))

    # SIMULATION surface rescale and render on SCREEN
    simulation_render = pygame.transform.scale(SIMULATION, SCREEN_SIZE)
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(simulation_render)
    pygame.display.update()
