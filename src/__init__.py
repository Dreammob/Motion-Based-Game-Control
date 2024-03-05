import cv2
import mediapipe as mp
import numpy as np
import collections
import time
import warnings    
warnings.simplefilter('ignore', np.RankWarning)
from util import *
from actions import Dodge, Jump

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# predefined pose classifier
#pose_classifier = PoseClassifier()


cap = cv2.VideoCapture(0)


# attack variables
attack_counter = 0 
dodge_counter = 0
block_counter = 0

# movement variables
direction = None
jump_counter = 0

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # For debugging purposes
    movement_stage = "none"
    attack_stage = "none"

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

            # Initialize action state objects
            jump_tracker = Jump()
            dodge_tracker = Dodge()

            # Final stages sent to integrator
            actions = []

            # Calculate angle for attack
            angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            
            # Visualize angle for arm
            """cv2.putText(image, str(angle), 
                            # replace 1280, 720 with camera feed resolution, finds location of elbow in actual feed
                           tuple(np.multiply(elbow, [1440, 980]).astype(int)), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                                """
            
            # action counter logic
            if left_wrist[0] < right_wrist[0] and left_wrist[1] < left_elbow[1] and right_wrist[1] < right_elbow[1]:
                attack_stage = "block"
                block_counter += 1
            elif l_r_dodge := dodge_tracker.update(new_left_shoulder_x_val=left_shoulder[0], new_timestamp=time.time()):
                attack_stage = l_r_dodge
                dodge_counter += 1
            elif angle > 160:
                attack_stage = "attack"
            elif angle < 30 and attack_stage =='attack':
                attack_stage = "prepare"
                attack_counter += 1
            
            # leg angles
            left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
            right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)

            # leg counter logic 
            cv2.putText(image, "left" + str(left_leg_angle), 
                            # replace 1280, 720 with camera feed resolution, finds location of elbow in actual feed
                           tuple(np.multiply(left_elbow, [1440, 980]).astype(int)), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, "right" + str(right_leg_angle), 
                            # replace 1280, 720 with camera feed resolution, finds location of elbow in actual feed
                           tuple(np.multiply(left_elbow, [1280, 720]).astype(int)), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            if (left_leg_angle < 140 and right_leg_angle > 140) or (right_leg_angle < 140 and left_leg_angle > 140):
                movement_stage = "run"
            elif(left_leg_angle < 150 and right_leg_angle > 150) or (right_leg_angle < 150 and left_leg_angle > 150):
                movement_stage = "walk"
            else:
                # jump logic
                if jump := jump_tracker.update(new_left_hip_y=left_hip[1], new_right_hip_y=right_hip[1], new_timestamp=time.time()):
                   movement_stage = jump

                if jump == 'jump':
                    jump_counter += 1

            actions.append(attack_stage)
            actions.append(movement_stage)
        except:
            pass

        # Setup status box
        cv2.rectangle(image, (0,0), (400,200), (245,117,16), -1)
        
        # data
        """ cv2.putText(image, 'Count', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        """
        cv2.putText(image, 'movement status: ' + movement_stage, (5,30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, 'jump counter: ' + str(jump_counter), (5,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, 'dodge counter: ' + str(dodge_counter), (5,90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, 'attack status: ' + attack_stage, (5,120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, 'attack counter: ' + str(attack_counter), (5,150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, 'block counter: ' + str(jump_counter), (5,180), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
