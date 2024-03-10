from dataclasses import dataclass

@dataclass
class CommandStringsConfig:
    # attacks
    attack_norm_left = "attack_norm_left"
    attack_norm_right = "attack_norm_right"
    attack_skill = "attack_skill"
    prepare = "prepare"

    # movements
    idle = "idle"
    walk = "walk"
    run = "run"
    dodge_left = "dodge_left"
    dodge_right = "dodge_right"
    jump = "jump"
    turn_left = "turn_left"
    turn_right = "turn_right"
    turn_no = "turn_no"