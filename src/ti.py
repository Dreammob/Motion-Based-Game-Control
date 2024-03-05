# Contains utility functions used across the project.

import cv2
import mediapipe as mp
import numpy as np


def calculate_angle(a,b,c):
    # returns the joint angles between points
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    rads = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(rads*180.0/np.pi)
    if angle > 180.0:
        angle = 360.0 - angle 
    return angle

