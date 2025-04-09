import pygame
import sys
import numpy as np
from random import randint
from math import e


pygame.init()

pygame.display.set_caption("Particle Life")

SCREEN = pygame.display.set_mode((1280, 720))
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = pygame.display.get_window_size()
SIMULATION = pygame.Surface((1280, 720))
SIMULATION_WIDTH, SIMULATION_HEIGHT = SIMULATION_SIZE = SIMULATION.get_size()
CLOCK = pygame.Clock()
deltatime = 0

# particles forces setups
force_decay = 100

# particles amount
PARTICLES_GROUPS = 2
PARTICLES_AMOUNT = 1000
PARTICLES_GROUP = int(PARTICLES_AMOUNT / PARTICLES_GROUPS)

def start():
    # particles groups
    global particles_position, particles_velocity, particles_render, particles_matrix
    particles_position = np.array([
        np.random.choice(np.arange(0, SIMULATION_WIDTH), size=PARTICLES_GROUP * PARTICLES_GROUPS),
        np.random.choice(np.arange(0, SIMULATION_HEIGHT), size=PARTICLES_GROUP * PARTICLES_GROUPS)
    ])

    particles_velocity = np.array([
        np.zeros(PARTICLES_GROUP * PARTICLES_GROUPS),
        np.zeros(PARTICLES_GROUP * PARTICLES_GROUPS)
    ])
    particles_render = np.array([pygame.Surface((1, 1)) for _ in range(0, PARTICLES_GROUPS)])

    # interaction matrix
    particles_matrix = np.array([
        np.random.choice(np.arange(-100, 101), size=PARTICLES_GROUPS),
        np.random.choice(np.arange(-100, 101), size=PARTICLES_GROUPS)
    ])


start()

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
        distances = np.sqrt(((delta_x ** 2) + (delta_y ** 2)))
        directions = np.nan_to_num(np.array([delta_x / distances, delta_y / distances]), nan=0.0)

        # to do: set 1 to particles_attraction
        forces = (1 * (e ** -(distances / force_decay))) * directions
        acceleration = np.array([np.sum(forces[0]), np.sum(forces[1])])

        particles_velocity[0][particle] += acceleration[0] * deltatime
        particles_velocity[1][particle] += acceleration[1] * deltatime

        velocity_x = particles_position[0][particle] + (particles_velocity[0][particle] * deltatime)
        velocity_y = particles_position[1][particle] + (particles_velocity[1][particle] * deltatime)

        if velocity_x > SIMULATION_WIDTH - 1 or velocity_x < 0:
            particles_velocity[0][particle] = -particles_velocity[0][particle]
            velocity_x = particles_position[0][particle] + (particles_velocity[0][particle] * deltatime)

        if velocity_y > SIMULATION_HEIGHT - 1 or velocity_y < 0:
            particles_velocity[1][particle] = -particles_velocity[1][particle]
            velocity_y = particles_position[1][particle] + (particles_velocity[1][particle] * deltatime)

        particles_position[0][particle] = velocity_x
        particles_position[1][particle] = velocity_y


while True:
    # events handling
    for event in pygame.event.get():
        # closes program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key down
        if event.type == pygame.KEYDOWN:
            # randomize particles (fix this later)
            if event.key == pygame.K_r:
                start()
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
    deltatime = CLOCK.tick(24) / 1000
