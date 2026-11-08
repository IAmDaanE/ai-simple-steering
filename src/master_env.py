import math
import pygame
import random

pygame.init()

class MasterEnv:
    def __init__(self):
        self.window_width = 700
        self.window_height = 400
        self.center_pos = (self.window_width / 2, self.window_height / 2)
        self.agent_img = pygame.transform.scale_by(pygame.image.load("../assets/agent.png"), 1)
        self.target_pos = ()
        self.target_dist = 170
        self.target_radius = 20
        self.font = pygame.font.Font("../assets/PressStart2P-Regular.ttf", 13)
        self.agent_envs = []
        self.num_frames = 0

    def move_target(self):
        target_angle = random.randint(0, 360)
        x_cord = self.center_pos[0] + (math.cos(math.radians(target_angle))) * self.target_dist
        y_cord = self.center_pos[1] + (math.sin(math.radians(target_angle))) * self.target_dist
        self.target_pos = (x_cord, y_cord)

    def render(self, game_surface):
        pygame.draw.circle(game_surface, (0, 0, 255), self.target_pos, self.target_radius)
        pygame.draw.circle(game_surface, (0, 0, 0), self.center_pos, 2)

    def render_text(self, game_surface, generation):
        generation_text = self.font.render(f"Generation: {generation}", True, (0,0,0))
        game_surface.blit(generation_text, (self.window_width / 2 - generation_text.get_width() / 2, 50))

    def step(self):
        self.num_frames += 1