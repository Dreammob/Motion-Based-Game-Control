"""Keeps track of when a user has performed a jumping maneuver."""
import collections
import numpy as np
from typing import Optional
from statistics import mean

JUMP_L_R_HIP_PIXEL_DIFF_THRESH = 10
JUMP_QUAD_REGRESS_A_THRESH = 2.0e-11
JUMP_NUM_FRAMES_TO_PROCESS = 30

# A naive method to detect jumping using quadratic regression. Maybe make length of queue dependent on time rather than frames?


class Jump:
    def __init__(self):
        # A naive method to detect jumping using quadratic regression. Maybe make length of queue dependent on time rather than frames?
        self._timestamps = collections.deque(JUMP_NUM_FRAMES_TO_PROCESS*[0], JUMP_NUM_FRAMES_TO_PROCESS)
        self._jump_hip_y_values = collections.deque(JUMP_NUM_FRAMES_TO_PROCESS*[(0, 0)], JUMP_NUM_FRAMES_TO_PROCESS)  

    
    def update(self, new_left_hip_y: int, new_right_hip_y: int, new_timestamp: int) -> Optional[str]:
        self._timestamps.append(new_timestamp)    
        self._jump_hip_y_values.append((new_left_hip_y, new_right_hip_y))

        calc_quad_regress = True
        for ys in self._jump_hip_y_values:
            if abs(ys[0] - ys[1]) >= JUMP_L_R_HIP_PIXEL_DIFF_THRESH:
                calc_quad_regress = False
                break
        
        stage = None
        if calc_quad_regress:
            hip_avgs = [(x[0] + x[1]) / 2 for x in self._jump_hip_y_values]
            quad_regress = np.poly1d(np.polyfit(self._timestamps, hip_avgs, 2))

        if quad_regress.coeffs[0] >= JUMP_QUAD_REGRESS_A_THRESH:
            stage = "jump"

        # print(quad_regress.coeffs[0], stage)
        
        return stage

