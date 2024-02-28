import cv2
import numpy as np
import mediapipe as mp
import traceback
from .utils import (
    get_landmark_coordinates,
    calculate_angle,
    log_landmark,
    log_angle,
    calculate_slope,
    compare_nums,
)
from .arm import ArmsState
from .leg import LegsState
from .face import FaceState
from .events import Events
from .const import IMAGE_HEIGHT, IMAGE_WIDTH, DRIVING_UP_AREA

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
