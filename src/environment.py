import random
import pygame
import math

class AgentEnv:
    def __init__(self, master_env):
        self.x = master_env.center_cord[0]
        self.y = master_env.center_cord[1]
        self.master_env = master_env
        self.rotation = random.randint(0, 360)
        self.rotation_speed = 5
        self.speed = 4
        self.fitness_score = 0

    def render(self, screen):
        rotated_img = pygame.transform.rotate(master_env.agent_img, self.rotation)
        rotated_rect = rotated_img.get_rect(center=master_env.agent_img.get_rect(topleft=(self.x, self.y)).center)
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

    def get_state(self):
        rel_x = (self.master_env.target_pos[0] - self.x) / self.master_env.window_width
        rel_y = (self.master_env.target_pos[1] - self.y) / self.master_env.window_height
        return [rel_x, rel_y]

class MasterEnv:
    def __init__(self):
        self.window_width = 600
        self.window_height = 600
        self.center_pos = (self.window_width / 2, self.window_height / 2)
        self.agent_img = pygame.transform.scale_by(pygame.image.load("../assets/agent.png"), 1)
        self.target_pos = ()
        self.target_dist = 200
        self.target_radius = 6

    def move_target(self):
        target_angle = random.randint(0, 360)
        x_cord = self.center_pos[0] + math.cos(math.radians(target_angle))
        y_cord = self.center_pos[1] + math.sin(math.radians(target_angle))
        self.target_pos = (x_cord, y_cord)

    def render(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), self.target_pos, self.target_radius)
        pygame.draw.circle(screen, (0, 0, 0), self.center_pos, 2)