from barebones_neat import InferenceVisualization, PreTrainedNEAT
import pygame
import argparse
from pathlib import Path

from agent_env import AgentEnv
from master_env import MasterEnv

parser = argparse.ArgumentParser(
        description="Train an MNIST prediction model."
    )

parser.add_index = parser.add_argument(
        "model_path", 
        type=str, 
        help="The path to the folder where the resulting trained model will be saved (e.g., ../models/v1)."
    )

args = parser.parse_args()
model_path = Path(args.model_path)

master_env = MasterEnv()
master_env.move_target()
master_env.agent_envs.append(AgentEnv(master_env))

pygame.init()
screen = pygame.display.set_mode((master_env.window_width, master_env.window_height + 140), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("NEAT Model Inference")

vis = InferenceVisualization(master_env.window_width, master_env.window_height, screen, ["rel angle"], ["left", "straight", "right"])

game_surface = pygame.Surface((master_env.window_width, master_env.window_height))

network = PreTrainedNEAT(model_path)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_surface.fill((255, 255, 255))

    if master_env.agent_envs[0].done:
        master_env.agent_envs[0] = AgentEnv(master_env)
        master_env.move_target()

    outputs = network.forward(master_env.agent_envs[0].get_state())
    action = outputs.index(max(outputs))
    master_env.agent_envs[0].step(action)

    master_env.render(game_surface)
    master_env.agent_envs[0].render(game_surface)

    vis.full_draw(network.compiled_genome, network, network_hor_padding=80, left_names_offset=64, right_names_offset=8, vert_names_offset=8, network_weight_mult=75, max_line_thickness=11)
    screen.blit(game_surface, (0, 0))

    pygame.display.update()