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
force_decay = 50

# particles amount
PARTICLES_GROUPS = 2
PARTICLES_AMOUNT = 200
PARTICLES_GROUP = int(PARTICLES_AMOUNT / PARTICLES_GROUPS)

# particles groups
particles_position = np.array([np.array([randint(0, SIMULATION_WIDTH - 1) for _ in range(0, PARTICLES_GROUP * PARTICLES_GROUPS)]), np.array([randint(0, SIMULATION_HEIGHT - 1) for _ in range(0, PARTICLES_GROUP * PARTICLES_GROUPS)])])
particles_velocity = np.array([np.zeros(PARTICLES_GROUP * PARTICLES_GROUPS), np.zeros(PARTICLES_GROUP * PARTICLES_GROUPS)])
particles_render = np.array([pygame.Surface((1, 1)) for _ in range(0, PARTICLES_GROUPS)])

# interaction matrix
particles_attraction = np.random.randint(-100, 101, (PARTICLES_GROUPS, PARTICLES_GROUP))

# setting color to particles groups
color_range = int(355 / PARTICLES_GROUPS)
color_value = 0
color = pygame.Color(0)
for i in range(0, PARTICLES_GROUPS):
    color.hsla = (color_value, 100, 50, 100)
    particles_render[i].fill((color.r, color.g, color.b, color.a))
    color_value += color_range

def accelaration():
    # I hate physics

    for particle in range(0, PARTICLES_GROUP * PARTICLES_GROUPS):
        delta_x = particles_position[0, :] - particles_position[0, particle]
        delta_y = particles_position[1, :] - particles_position[1, particle]
        distances = ((delta_x ** 2) + (delta_y ** 2)) ** 0.5
        directions = np.nan_to_num(np.array([delta_x / distances, delta_y / distances]), nan=0.0)

        # to do: set 1 to particles_attraction
        forces = (1 * (e ** -(distances / force_decay))) * directions
        acceleration = np.array([np.sum(forces[0]), np.sum(forces[1])])

        acceleration_x = particles_position[0][particle] + acceleration[0]
        acceleration_y = particles_position[1][particle] + acceleration[1]
        if acceleration_x > SIMULATION_WIDTH - 1 or acceleration_x < 0:
            acceleration_x = -acceleration_x

        if acceleration_y > SIMULATION_WIDTH - 1 or acceleration_y < 0:
            acceleration_y = -acceleration_y

        particles_position[0][particle] = acceleration_x
        particles_position[1][particle] = acceleration_y


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
                particles_position = np.array(
                    [np.array([randint(0, SIMULATION_WIDTH - 1) for _ in range(0, PARTICLES_GROUP * PARTICLES_GROUPS)]),np.array([randint(0, SIMULATION_HEIGHT - 1) for _ in range(0, PARTICLES_GROUP * PARTICLES_GROUPS)])])
    accelaration()
    # particles render in SIMULATION surface
    SIMULATION.fill((0, 0, 0))
    for group in range(0, PARTICLES_GROUPS):
        # probably works good (I have no idea)
        for particle in range(group * PARTICLES_GROUP, group * PARTICLES_GROUP + PARTICLES_GROUP):
            SIMULATION.blit(particles_render[group], (particles_position[0, particle], particles_position[1, particle]))

    # SIMULATION surface rescale and render on SCREEN
    simulation_render = pygame.transform.scale(SIMULATION, SCREEN_SIZE)
    SCREEN.blit(simulation_render)
    pygame.display.update()
    CLOCK.tick(24)
