"""Keeps track of when a user has performed a dodge maneuver."""
import collections
import numpy as np
from typing import Optional

DODGE_LIN_REGRESS_A_THRESH = 1e-4  # arbitrary: needs testing
DODGE_NUM_FRAMES_TO_PROCESS = 60

# A naive method to detect jumping using quadratic regression. Maybe make length of queue dependent on time rather than frames?


class Dodge:
    def __init__(self):
        self._timestamps = collections.deque(DODGE_NUM_FRAMES_TO_PROCESS*[0], DODGE_NUM_FRAMES_TO_PROCESS)
        self._left_shoulder_x_values = collections.deque(DODGE_NUM_FRAMES_TO_PROCESS*[0], DODGE_NUM_FRAMES_TO_PROCESS)  
    
    def update(self, new_left_shoulder_x_val: int, new_timestamp: int) -> Optional[str]:
        self._left_shoulder_x_values.append(new_left_shoulder_x_val)
        self._timestamps.append(new_timestamp)

        lin_regress = np.poly1d(np.polyfit(self._timestamps, self._left_shoulder_x_values, 1))

        def zero_array(arr):
            for i in range(len(arr)):
                arr[i] = 0

        if lin_regress.coeffs[0] >= DODGE_LIN_REGRESS_A_THRESH:
            zero_array(self._left_shoulder_x_values)
            return "dodge_left"
        elif lin_regress.coeffs[0] <= -DODGE_LIN_REGRESS_A_THRESH:
            zero_array(self._left_shoulder_x_values)
            return "dodge_right"
        else:
            return None

