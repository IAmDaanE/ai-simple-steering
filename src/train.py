from barebones_neat import NEAT, TrainingVisualization
from master_env import MasterEnv
from agent_env import AgentEnv
import pygame
import sys
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
        description="Train a NEAT model."
    )

parser.add_index = parser.add_argument(
        "model_path", 
        type=str, 
        help="The relative path to the folder where the resulting trained model will be saved (e.g., ../models/v1)."
    )

args = parser.parse_args()
model_path = Path(args.model_path)

pygame.init()

generation = 1
population_size = 60
alive = population_size
max_frames = 10000

neat = NEAT(population_size=population_size, 
            input_size=1,
            output_size=3, 
            crossover_chance=60, 
            new_node_chance=0, 
            new_connection_chance=25, 
            change_weight_chance=50, 
            change_bias_chance=25, 
            mutation_power=0.08, 
            similarity_treshold=0.5, 
            excess_mult=1.0, 
            disjoint_mult=1.0, 
            weight_dif_mult=0.4, 
            use_softmax=True)

neat.compile_genomes()

master_env = MasterEnv()

master_env.move_target()
for i, specie in enumerate(neat.species):
    master_env.agent_envs.append([])
    for q, genome in enumerate(specie):
        master_env.agent_envs[i].append([])
        master_env.agent_envs[i][q] = AgentEnv(master_env)

screen = pygame.display.set_mode((master_env.window_width, master_env.window_height + 140), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("NEAT Training")
game_surface = pygame.Surface((master_env.window_width, master_env.window_height))
running = True

vis = TrainingVisualization(master_env.window_width, master_env.window_height, screen, ["rel angle"], ["left", "straight", "right"])

while running:
    try:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_surface.fill((255, 255, 255))

        for i, specie in enumerate(master_env.agent_envs):
            for q, env in enumerate(specie):
                if env.done:
                    if not env.handled_death:
                        alive -= 1
                        neat.species[i][q]["fitness_score"] = env.fitness_score
                        env.handled_death = True
                    else:
                        continue
                else:
                    outputs = neat.species[i][q]["compiled_genome_class"].forward(master_env.agent_envs[i][q].get_state())    
                    action = outputs.index(max(outputs))
                    env.step(action)
                    env.render(game_surface)

        if master_env.num_frames >= max_frames:
            for i, specie in enumerate(master_env.agent_envs):
                for q, env, in enumerate(specie):
                    env.done = True
            master_env.num_frames = 0
        
        master_env.step()
        master_env.render(game_surface)
        master_env.render_text(game_surface, generation)
        
        if alive == 0:
            best_genome_class = neat.get_best_agent()["compiled_genome_class"]
            screen.fill((255, 255, 255))
            vis.full_draw(best_genome_class, neat, network_hor_padding=80, left_names_offset=64, right_names_offset=8, vert_names_offset=8, max_line_thickness=11)
            neat.create_new_generation()
            neat.sort_into_species()
            neat.genome_pool.clear()
            master_env.agent_envs.clear()
            master_env.move_target()
            alive = population_size
            for i, specie in enumerate(neat.species):
                master_env.agent_envs.append([])
                for genome in specie:
                    master_env.agent_envs[i].append(AgentEnv(master_env))
            generation += 1
            neat.compile_genomes()

        screen.blit(game_surface, (0, 0))
        pygame.display.update()
    except KeyboardInterrupt:
        neat.save_model(model_path)
        sys.exit()