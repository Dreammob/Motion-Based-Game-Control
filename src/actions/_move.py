"""Keeps track of when a user has performed a normal attack."""
import time
from typing import Optional

class Move:
    def __init__(self, walk_threshold: int, run_threshold: int):
        self.walk_threshold = walk_threshold
        self.run_threshold = run_threshold
        self.state_lock_duration = 1 # Duration in seconds to lock the state
        self.state = "idle"
        self.last_state_change_time = time.time()  # Timestamp of the last state change

    def update(self, left_leg_angle, right_leg_angle) -> Optional[str]:
        current_time = time.time()
        time_since_last_change = current_time - self.last_state_change_time
        
        # If the state is locked, return the current state without updating
        if self.state in ["walk", "run"] and time_since_last_change < self.state_lock_duration:
            return self.state

        # Update the state based on leg angles
        if left_leg_angle < self.run_threshold or right_leg_angle < self.run_threshold  :
            new_state = "run"
        elif left_leg_angle < self.walk_threshold or right_leg_angle < self.walk_threshold:
            new_state = "walk"
        elif left_leg_angle >= self.walk_threshold and right_leg_angle >= self.walk_threshold:
            new_state = "idle"

        # If the state has changed, update the state and reset the last_state_change_time
        if new_state != self.state:
            self.state = new_state
            self.last_state_change_time = current_time

        return self.state
