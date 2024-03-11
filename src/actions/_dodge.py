"""Keeps track of when a user has performed a dodge maneuver: moving to the left or right of the screen quickly."""
import collections
import numpy as np
from typing import Optional
from statistics import mean
from enum import Enum
from command_strings_config import CommandStringsConfig

DODGE_NUM_FRAMES_TO_PROCESS = 30

DODGE_LEFT_LIN_REGRESS_A_THRESH = 0.11
DODGE_RIGHT_LIN_REGRESS_A_THRESH = -0.11

DODGE_LEFT_PIXEL_THRESH = 0.80
DODGE_RIGHT_PIXEL_THRESH = 0.40

class Dodge:
    def __init__(self, left_pixel_thresh=DODGE_LEFT_PIXEL_THRESH, right_pixel_thresh=DODGE_RIGHT_PIXEL_THRESH):
        self._timestamps = collections.deque(DODGE_NUM_FRAMES_TO_PROCESS*[0], DODGE_NUM_FRAMES_TO_PROCESS)
        self._left_shoulder_x_values = collections.deque(DODGE_NUM_FRAMES_TO_PROCESS*[0], DODGE_NUM_FRAMES_TO_PROCESS) 
        self._last_dodge_time = None
        self._left_pixel_thresh = left_pixel_thresh
        self._right_pixel_thresh = right_pixel_thresh
    
    def update(self, new_left_shoulder_x_val: int, new_timestamp: int) -> Optional[str]:
        # moving right gives lower pixel value
        # moving left gives higher pixel value
        self._left_shoulder_x_values.append(new_left_shoulder_x_val)
        self._timestamps.append(new_timestamp)

        lin_regress = np.poly1d(np.polyfit(self._timestamps, self._left_shoulder_x_values, 1))

        state = None
        a = lin_regress.coeffs[0]
        if a > DODGE_LEFT_LIN_REGRESS_A_THRESH and self._left_pixel_thresh <= new_left_shoulder_x_val <= 1.0:
            state = CommandStringsConfig.dodge_left
        elif a < DODGE_RIGHT_LIN_REGRESS_A_THRESH and 0.0 <= new_left_shoulder_x_val <= self._right_pixel_thresh:
            state = CommandStringsConfig.dodge_right
        
        return state

