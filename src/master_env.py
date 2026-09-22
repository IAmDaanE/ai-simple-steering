import math
import pygame
import random

class MasterEnv:
    def __init__(self):
        self.window_width = 600
        self.window_height = 600
        self.center_pos = (self.window_width / 2, self.window_height / 2)
        self.agent_img = pygame.transform.scale_by(pygame.image.load("../assets/agent.png"), 1)
        self.target_pos = ()
        self.target_dist = 140
        self.target_radius = 20
        self.font = pygame.font.Font("../assets/PressStart2P-Regular.ttf")
        self.agent_envs = []
        self.num_frames = 0

    def move_target(self):
        target_angle = random.randint(0, 360)
        x_cord = self.center_pos[0] + (math.cos(math.radians(target_angle))) * self.target_dist
        y_cord = self.center_pos[1] + (math.sin(math.radians(target_angle))) * self.target_dist
        self.target_pos = (x_cord, y_cord)

    def render(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), self.target_pos, self.target_radius)
        pygame.draw.circle(screen, (0, 0, 0), self.center_pos, 2)

    def step(self):
        self.num_frames += 1