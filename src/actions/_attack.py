"""Keeps track of when a user has performed a normal attack."""
from typing import Optional
from command_strings_config import CommandStringsConfig

class Attack:
    def __init__(self, attack_threshold: int):
        self.attack_threshold = attack_threshold

    def update_left(self, left_angle) -> Optional[str]:
        if left_angle > self.attack_threshold:
            return CommandStringsConfig.left_attack_norm
        else:
            return CommandStringsConfig.prepare
    def update_right(self, right_angle) -> Optional[str]:
        if right_angle > self.attack_threshold:
            return CommandStringsConfig.right_attack_norm
        else:
            return CommandStringsConfig.prepare
