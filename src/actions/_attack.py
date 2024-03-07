"""Keeps track of when a user has performed a normal attack."""
from typing import Optional
from command_strings_config import CommandStringsConfig

class Attack:
    def __init__(self, attack_threshold: int):
        self.attack_threshold = attack_threshold

    def update(self, angle, left_elbow, left_wrist, right_elbow, right_wrist) -> Optional[str]:

        if angle > self.attack_threshold:
            return CommandStringsConfig.attack_norm
        elif left_wrist[0] < right_wrist[0] and left_wrist[1] < left_elbow[1] and right_wrist[1] < right_elbow[1]:
            return CommandStringsConfig.attack_skill
        else:
            return CommandStringsConfig.prepare