import pygame
import math
import random
from utils import get_dist_to_target, get_rel_angle_to_target

class AgentEnv:
    def __init__(self, master_env):
        self.x = master_env.center_pos[0]
        self.y = master_env.center_pos[1]
        self.master_env = master_env
        self.rotation = random.randint(0, 360)
        self.rotation_speed = 18
        self.speed = 0.5
        self.fitness_score = 0
        self.dist_to_target = get_dist_to_target((self.x, self.y), self.master_env.target_pos)
        self.prev_rel_angle = get_rel_angle_to_target((self.x, self.y), master_env.target_pos, self.rotation)
        self.done = False
        self.handled_death = False

    def render(self, game_surface):
        rotated_img = pygame.transform.rotate(self.master_env.agent_img, self.rotation - 90)
        rotated_rect = rotated_img.get_rect(center=self.master_env.agent_img.get_rect(topleft=(self.x, self.y)).center)
        game_surface.blit(rotated_img, rotated_rect.topleft)

    def step(self, action):
        if action == 0:    # turn left
            self.rotation -= self.rotation_speed
        elif action == 1:  # go straight
            pass
        else:              # turn right
            self.rotation += self.rotation_speed

        if self.rotation < 0:
            self.rotation += 360
        if self.rotation > 360:
            self.rotation -= 360

        x_move =  math.cos(math.radians(self.rotation)) * self.speed
        y_move =  -math.sin(math.radians(self.rotation)) * self.speed
        self.x += x_move
        self.y += y_move

        if self.x < 0 or self.x > self.master_env.window_width or self.y < 0 or self.y  > self.master_env.window_height:
            self.done = True

        self.dist_to_target = get_dist_to_target((self.x, self.y), self.master_env.target_pos)

        if self.dist_to_target < self.master_env.target_radius:
            self.done = True
            self.fitness_score += 500
        if abs(self.prev_rel_angle) > abs(get_rel_angle_to_target((self.x, self.y), self.master_env.target_pos, self.rotation)):
            self.fitness_score += 1
        else:
            self.fitness_score -= 1

    def get_state(self):
        rel_angle_to_target = get_rel_angle_to_target((self.x, self.y), self.master_env.target_pos, self.rotation)
        return [rel_angle_to_target / 180]