"""tracks the user preforming a turn"""
from typing import Optional

class Turn:
    def __init__(self, left_turn_threshold: int, right_turn_threshold: int):
        self.left_turn_threshold = left_turn_threshold
        self.right_turn_threshold = right_turn_threshold
        self.state = "No Turn"

    def update(self, turn_angle: int) -> Optional[str]:
        if self.right_turn_threshold > turn_angle:
            self.state = "right turn"
        elif turn_angle > self.left_turn_threshold:
            self.state = "left turn"
        elif turn_angle <+ self.left_turn_threshold or self.right_turn_threshold <= turn_angle:
            self.state = "No turn"
        return self.state
