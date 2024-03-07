import cv2
import mediapipe as mp
import numpy as np
import collections
import time
import warnings    
warnings.simplefilter('ignore', np.RankWarning)
from util import *

from datetime import datetime
from actions import Dodge, Jump, NAttack, Move, Turn

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize action state objects
jump_tracker = Jump()
dodge_tracker = Dodge()
nAttack_tracker = NAttack(attack_threshold = 160) # angle which when greater counts as attack
move_tracker = Move(walk_threshold = 165, run_threshold = 145)
turn_tracker = Turn(left_turn_threshold = 125, right_turn_threshold=95)


cap = cv2.VideoCapture(0)


# attack variables 
# still needed?
attack_counter = 0 
dodge_counter = 0
block_counter = 0

# movement variables
direction = None
jump_counter = 0

def write_action_to_file(actions):
    with open("command_flag.txt", "a") as file:  # 'a' mode for appending
        now = datetime.now()
        # Include milliseconds in the time format (%f is microseconds, so we slice to get milliseconds)
        current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Truncate microseconds to milliseconds
        formatted_actions = ' - '.join(actions)  # Join actions with ' - ' as separator
        # Write both the datetime and formatted actions
        file.write(f"{current_time} || {formatted_actions}\n")


## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            left_ear = [landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y]
            right_ear = [landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y]
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            left_mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y]
            right_mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].y]



            # Final stages sent to integrator
            actions = []

            # Calculate angles for attack, turn and move
            attack_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            left_leg_angle = calculate_angle(left_ankle, left_knee, left_hip)
            right_leg_angle = calculate_angle(right_ankle, right_knee, right_hip)
            turn_angle = calculate_angle(right_ear, nose, left_shoulder)
            # right_turn_angle = calculate_angle(left_ear, nose, right_shoulder)

            # Visualize angle if needed
            cv2.putText(image, str(left_leg_angle), 
                            # replace 1280, 720 with camera feed resolution, finds location of elbow in actual feed
                           (100,500), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                                
            # identify and add to actions
            move_state = move_tracker.update(left_leg_angle, right_leg_angle)
            attack_state = nAttack_tracker.update(attack_angle)
            turn_state = turn_tracker.update(turn_angle)
            actions.append(turn_state)
            actions.append(attack_state)
            actions.append(move_state)

          
            if left_wrist[0] < right_wrist[0] and left_wrist[1] < left_elbow[1] and right_wrist[1] < right_elbow[1]:
                attack_stage = "block"
                block_counter += 1
                # above still needed?
                actions.append("block")
            elif l_r_dodge := dodge_tracker.update(new_left_shoulder_x_val=left_shoulder[0], new_timestamp=time.time()):
                attack_stage = l_r_dodge
                dodge_counter += 1
                # above still needed?
                actions.append("dodge")
            # jump logic
            if jump := jump_tracker.update(new_left_hip_y=left_hip[1], new_right_hip_y=right_hip[1], new_timestamp=time.time()):
                movement_stage = jump

            if jump == 'jump':
                jump_counter += 1
                actions.append("jump")

                                
            # Setup status box
            cv2.rectangle(image, (0,0), (400,200), (245,117,16), -1)
            
            # data
            """ cv2.putText(image, 'Count', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            """
            cv2.putText(image, 'movement status: ' + move_state, (5,30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image, 'attack status: ' + attack_state, (5,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image, 'turn status: ' + turn_state, (5,90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

            """ cv2.putText(image, 'jump counter: ' + str(jump_counter), (5,120), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image, 'dodge counter: ' + str(dodge_counter), (5,), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image, 'block counter: ' + str(jump_counter), (5,180), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                    """

                                
            write_action_to_file(actions)
            """  just pass action to integrator in the end   
            Instead of printing or just setting stage, write the action directly to the file
            if attack_stage == "attack":
                write_action_to_file('01')
            elif stage == "prepare":
                write_action_to_file('00')  # Assuming you want to track this stage as well
            elif stage == "jumping":
                write_action_to_file('jump')
            # Add more elif blocks for other stages/actions as necessary """
                
        except:
            pass


        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
