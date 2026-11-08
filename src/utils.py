import math

def get_dist_to_target(agent_pos, target_pos):
    x_dist = abs(agent_pos[0] - target_pos[0])
    y_dist = abs(agent_pos[1] - target_pos[1])
    return math.sqrt(x_dist ** 2 + y_dist ** 2)

def get_rel_angle_to_target(agent_pos, target_pos, agent_angle):
    dx = target_pos[0] - agent_pos[0]
    dy = target_pos[1] - agent_pos[1]
    angle_to_target = math.degrees(math.atan2(-dy, dx))
    rel_angle = angle_to_target - agent_angle
    rel_angle = (rel_angle + 180) % 360 - 180
    return rel_angle