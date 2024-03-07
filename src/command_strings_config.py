from dataclasses import dataclass

@dataclass
class CommandStringsConfig:
    # attacks
    attack_norm = "attack_norm"
    attack_skill = "attack_skill"
    prepare = "prepare"

    # movements
    idle = "idle"
    walk = "walk"
    run = "run"
    dodge_left = "dodge_left"
    dodge_right = "dodge_right"
    jump = "jump"