from barebones_neat import NEAT
from environment import MasterEnv, AgentEnv
import pygame

pygame.init()
screen = pygame.display.set_mode((650, 400))
clock = pygame.time.Clock()
pygame.display.set_caption("AI Environment")

generation = 1
population_size = 300
alive = population_size

NEAT = NEAT(population_size, 4, 3, 60, 4, 21, 50, 25, 0.5, 0.5, 1.0, 1.0, 0.4)
NEAT.compile_genomes()

master_env = MasterEnv()
for i, specie in enumerate(NEAT.species):
    master_env.player_envs.append([])
    for q, genome in enumerate(specie):
        master_env.agent_envs[i].append([])
        master_env.player_envs[i][q] = AgentEnv(master_env)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))

    for i, specie in enumerate(master_env.agent_envs):
        for q, env in enumerate(specie):
            if env.done:
                if not env.handled_death:
                    alive -= 1
                    NEAT.species[i][q]["fitness_score"] = env.fitness_score
                    env.handled_death = True
                else:
                    continue
            else:
                outputs = NEAT.species[i][q]["compiled_genome_class"].forward(master_env.get_state())    
                action = outputs.index(max(outputs))
                env.step(action)
                env.render(screen)
    
    master_env.step()
    master_env.render_score_text(screen)
    master_env.render(screen)
    generation_text = master_env.big_font.render(f"Generation: {generation}", True, (0,0,0))
    screen.blit(generation_text, (master_env.window_width / 2 - generation_text.get_width() / 2, 120))
    
    if alive == 0:
        NEAT.create_new_generation()
        NEAT.sort_into_species()
        NEAT.genome_pool.clear()
        master_env.agent_envs.clear()
        master_env.reset()
        alive = 300
        for i, specie in enumerate(NEAT.species):
            master_env.agent_envs.append([])
            for genome in specie:
                master_env.agent_envs[i].append(AgentEnv(master_env))
        generation += 1
        NEAT.compile_genomes()
        print(f"specie distribution: {len(NEAT.species)}   | ", end=" ")
        for specie in NEAT.species:
            print(len(specie), end="   ")
        print("")

    pygame.display.update()