from dataclasses import dataclass

@dataclass
class CommandStringsConfig:
    # attacks
    left_attack_norm = "left_attack_norm"
    right_attack_norm = "right_attack_norm"
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