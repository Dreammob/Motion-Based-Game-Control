"""Keeps track of when a user has performed a dodge maneuver."""
import collections
import numpy as np
from typing import Optional
from statistics import mean
from enum import Enum
from util import FRAME_WIDTH

DODGE_NUM_FRAMES_TO_PROCESS = 30

DODGE_LEFT_LIN_REGRESS_A_THRESH = 0.12
DODGE_RIGHT_LIN_REGRESS_A_THRESH = -0.12

DODGE_LEFT_PIXEL_THRESH = 0.80
DODGE_RIGHT_PIXEL_THRESH = 0.40

class Dodge:
    def __init__(self):
        self._timestamps = collections.deque(DODGE_NUM_FRAMES_TO_PROCESS*[0], DODGE_NUM_FRAMES_TO_PROCESS)
        self._left_shoulder_x_values = collections.deque(DODGE_NUM_FRAMES_TO_PROCESS*[0], DODGE_NUM_FRAMES_TO_PROCESS) 
        self._last_dodge_time = None
    
    def update(self, new_left_shoulder_x_val: int, new_timestamp: int) -> Optional[str]:
        # moving right gives lower pixel value
        # moving left gives higher pixel value
        self._left_shoulder_x_values.append(new_left_shoulder_x_val)
        self._timestamps.append(new_timestamp)

        lin_regress = np.poly1d(np.polyfit(self._timestamps, self._left_shoulder_x_values, 1))

        stage = None
        a = lin_regress.coeffs[0]
        if a > DODGE_LEFT_LIN_REGRESS_A_THRESH and DODGE_LEFT_PIXEL_THRESH <= new_left_shoulder_x_val <= 1.0:
            stage = "dodge_left"
        elif a < DODGE_RIGHT_LIN_REGRESS_A_THRESH and 0.0 <= new_left_shoulder_x_val <= DODGE_RIGHT_PIXEL_THRESH:
            stage = "dodge_right"
        
        return stage

