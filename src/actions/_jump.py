"""Keeps track of when a user has performed a jumping maneuver: squatting and then standing back up quickly."""
import collections
import numpy as np
from typing import Optional
from command_strings_config import CommandStringsConfig

JUMP_QUAD_REGRESS_A_THRESH = 2.0e-11
JUMP_NUM_FRAMES_TO_PROCESS = 30

class Jump:
    def __init__(self):
        # A naive method to detect jumping using quadratic regression. Maybe make length of queue dependent on time rather than frames?
        self._timestamps = collections.deque(JUMP_NUM_FRAMES_TO_PROCESS*[0], JUMP_NUM_FRAMES_TO_PROCESS)
        self._jump_hip_y_values = collections.deque(JUMP_NUM_FRAMES_TO_PROCESS*[(0, 0)], JUMP_NUM_FRAMES_TO_PROCESS)  

    
    def update(self, new_left_hip_y: int, new_right_hip_y: int, new_timestamp: int) -> Optional[str]:
        self._timestamps.append(new_timestamp)    
        self._jump_hip_y_values.append((new_left_hip_y, new_right_hip_y))
        
        state = None
        hip_avgs = [(x[0] + x[1]) / 2 for x in self._jump_hip_y_values]
        quad_regress = np.poly1d(np.polyfit(self._timestamps, hip_avgs, 2))

        if quad_regress.coeffs[0] >= JUMP_QUAD_REGRESS_A_THRESH:
            state = CommandStringsConfig.jump

        # print(quad_regress.coeffs[0], state)
        
        return state

 