"""Keeps track of when a user has performed a turning left or right maneuver: turning shoulders left or right."""
from typing import Optional
from command_strings_config import CommandStringsConfig
class Turn:
    def __init__(self, turn_shoulder_pixel_diff_threshold: int):
        self._turn_threshold = turn_shoulder_pixel_diff_threshold
        
    def update(self, left_shoulder, right_shoulder, nose) -> Optional[str]:
        turn_state = None

        shoulder_pixel_diff = abs(left_shoulder[0] - right_shoulder[0])

        if shoulder_pixel_diff < self._turn_threshold and nose[0] < left_shoulder[0] and nose[0] < right_shoulder[0]:
            turn_state = CommandStringsConfig.turn_right
        elif shoulder_pixel_diff < self._turn_threshold and nose[0] > left_shoulder[0] and nose[0] > right_shoulder[0]:
            turn_state = CommandStringsConfig.turn_left


        return turn_state