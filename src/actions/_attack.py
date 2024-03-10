"""Keeps track of when a user has performed some attack: swinging left or right arm up and down = normal attack, X over chest = skill attack."""
from typing import Optional, List
from command_strings_config import CommandStringsConfig

class Attack:
    def __init__(self, attack_threshold: int):
        self.attack_threshold = attack_threshold

    def update(self, left_angle, right_angle, left_wrist, right_wrist, left_elbow, right_elbow) -> List[Optional[str]]:

        if left_wrist[0] < right_wrist[0] and left_wrist[1] < left_elbow[1] and right_wrist[1] < right_elbow[1]:
            return [CommandStringsConfig.attack_skill]

        left_and_right_states = []

        if left_angle > self.attack_threshold:
            left_and_right_states.append(CommandStringsConfig.attack_norm_left)
        else:
            return [CommandStringsConfig.prepare]

        if right_angle > self.attack_threshold:
            left_and_right_states.append(CommandStringsConfig.attack_norm_right)
        else:
            return [CommandStringsConfig.prepare]
        
        return left_and_right_states
