"""Keeps track of when a user has performed a normal attack."""
from typing import Optional

class NAttack:
    def __init__(self, attack_threshold: int):
        self.attack_threshold = attack_threshold

    def update(self, angle: int) -> Optional[str]:
        if angle > self.attack_threshold:
            return "attack"
        else:
            return "prepare"