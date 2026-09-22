import pygame
import math
from utils import get_dist_to_target, get_angle_to_target, corrected_pygame_angle

class AgentEnv:
    def __init__(self, master_env):
        self.x = master_env.center_pos[0]
        self.y = master_env.center_pos[1]
        self.master_env = master_env
        self.rotation = random.randint(0, 360)
        self.rotation_speed = 5
        self.speed = 1
        self.fitness_score = 0
        self.dist_to_target = get_dist_to_target((self.x, self.y), self.master_env.target_pos)
        self.prev_dist_to_target = self.dist_to_target
        self.done = False
        self.handled_death = False

    def render(self, screen):
        rotation = corrected_pygame_angle(self.rotation)
        rotated_img = pygame.transform.rotate(self.master_env.agent_img, rotation)
        rotated_rect = rotated_img.get_rect(center=self.master_env.agent_img.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_img, rotated_rect.topleft)

    def step(self, action):
        if action == 0: # turn left
            self.rotation -= self.rotation_speed
        elif action == 1: # go straight
            pass
        else:           # turn right
            self.rotation += self.rotation_speed

        if self.rotation < 0:
            self.rotation += 360
        if self.rotation > 360:
            self.rotation -= 360

        x_move = math.cos(math.radians(self.rotation)) * self.speed
        y_move = math.sin(math.radians(self.rotation)) * self.speed
        self.x += x_move
        self.y += y_move

        if self.x < 0 or self.x > self.master_env.window_width or self.y < 0 or self.y  > self.master_env.window_height:
            self.done = True

        self.dist_to_target = get_dist_to_target((self.x, self.y), self.master_env.target_pos)

        if self.dist_to_target < self.master_env.target_radius:
            self.done = True
            self.fitness_score += 100
        if self.dist_to_target < self.prev_dist_to_target:
            self.fitness_score += 1
        elif self.dist_to_target == self.prev_dist_to_target:
            self.fitness_score -= 0.4
        else:
            self.fitness_score -= 1
        self.prev_dist_to_target = self.dist_to_target

    def get_state(self):
        rel_x = (self.master_env.target_pos[0] - self.x) / self.master_env.window_width
        rel_y = (self.master_env.target_pos[1] - self.y) / self.master_env.window_height
        norm_rotation = self.rotation / 360
        return [rel_x, rel_y, norm_rotation]