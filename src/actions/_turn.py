"""tracks the user preforming a turn, normal turn angle should be around 110 - 120 ,
 less turn angle means head is more to the left, more turn angle means head is more to right"""
from typing import Optional
from command_strings_config import CommandStringsConfig
class Turn:
    # def __init__(self, left_turn_threshold: int, right_turn_threshold: int):
    #     self.left_turn_threshold = left_turn_threshold
    #     self.right_turn_threshold = right_turn_threshold
    #     self.state = "No Turn"

    # def update(self, turn_angle: int) -> Optional[str]:
    #     if self.right_turn_threshold > turn_angle:
    #         self.state = CommandStringsConfig.turn_right
    #     elif turn_angle > self.left_turn_threshold:
    #         self.state = CommandStringsConfig.turn_left
    #     elif turn_angle <= self.left_turn_threshold or self.right_turn_threshold <= turn_angle:
    #         self.state = CommandStringsConfig.turn_no
    #     return self.state

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