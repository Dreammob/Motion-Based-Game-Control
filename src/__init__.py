import cv2
import mediapipe as mp
import numpy as np
import collections
import time
import warnings    
warnings.simplefilter('ignore', np.RankWarning)
from util import *

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# predefined pose classifier
#pose_classifier = PoseClassifier()


cap = cv2.VideoCapture(0)


#attack variables
attack_counter = 0 
stage = None

#running variables
run_stage = "No Move"
direction = None

# jumping variables/constants
JUMP_L_R_HIP_PIXEL_DIFF_THRESH = 10
JUMP_QUAD_REGRESS_A_THRESH = 0
JUMP_NUM_FRAMES_TO_PROCESS = 60

jump_counter = 0

# A naive method to detect jumping using quadratic regression. Maybe make length of queue dependent on time rather than frames?
jump_hip_times = collections.deque(JUMP_NUM_FRAMES_TO_PROCESS*[0], JUMP_NUM_FRAMES_TO_PROCESS)
jump_hip_y_values = collections.deque(JUMP_NUM_FRAMES_TO_PROCESS*[(0, 0)], JUMP_NUM_FRAMES_TO_PROCESS)  

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
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # Final stages sent to integrator
            actions = []

            # Calculate angle for attack
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # Visualize angle for arm
            """cv2.putText(image, str(angle), 
                            # replace 1280, 720 with camera feed resolution, finds location of elbow in actual feed
                           tuple(np.multiply(elbow, [1440, 980]).astype(int)), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                                """
            
            # action counter logic
            if angle > 160:
                attack_stage = "attack"
            if angle < 30 and attack_stage =='attack':
                attack_stage = "prepare"
                attack_counter +=1

            actions.append(attack_stage)
            
            # leg angles
            left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
            right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)

            # leg counter logic 
            cv2.putText(image, "left" + str(left_leg_angle), 
                            # replace 1280, 720 with camera feed resolution, finds location of elbow in actual feed
                           tuple(np.multiply(elbow, [1440, 980]).astype(int)), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, "right" + str(right_leg_angle), 
                            # replace 1280, 720 with camera feed resolution, finds location of elbow in actual feed
                           tuple(np.multiply(elbow, [1280, 720]).astype(int)), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            if (left_leg_angle < 140 and right_leg_angle > 140) or (right_leg_angle < 140 and left_leg_angle > 140):
                movement_stage = "run"
            elif(left_leg_angle < 150 and right_leg_angle > 150) or (right_leg_angle < 150 and left_leg_angle > 150):
                movement_stage = "walk"
            else:
                # jump logic
                jump_hip_times.append(time.time())    
                jump_hip_y_values.append((left_hip[1], right_hip[1]))

                calc_quad_regress = True
                for ys in jump_hip_y_values:
                    if abs(ys[0] - ys[1]) >= JUMP_L_R_HIP_PIXEL_DIFF_THRESH:
                        calc_quad_regress = False
                        break
                
                if calc_quad_regress:
                    quad_regress = np.poly1d(np.polyfit(jump_hip_times, [(x[0] + x[1]) / 2 for x in jump_hip_y_values], 2))

                if quad_regress.coeffs[0] <= JUMP_QUAD_REGRESS_A_THRESH:
                    print("quad a when jump detected: ", quad_regress.coeffs[0])
                    movement_stage = "jump"
                    for i in range(len(jump_hip_y_values)):
                        jump_hip_y_values[i] = (0, 0)

                    jump_counter += 1
                else:
                    print("quad a when jump not detected: ", quad_regress.coeffs[0])
                    movement_stage = "stop"

        except:
            pass

        # Setup status box
        cv2.rectangle(image, (0,0), (400,140), (245,117,16), -1)
        
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
        cv2.putText(image, 'attack status: ' + attack_stage, (5,90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, 'attack counter: ' + str(attack_counter), (5,120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
