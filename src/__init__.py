import cv2
import mediapipe as mp
import numpy as np
from util import *
from datetime import datetime

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# predefined pose classifier
#pose_classifier = PoseClassifier()


cap = cv2.VideoCapture(0)


#attack variables
counter = 0 
stage = None

#jumping variables
left_hip_y = None
right_hip_y = None
threshold = 100

def write_action_to_file(action):
    with open("command_flag.txt", "a") as file:  # 'a' mode for appending
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Format the datetime
        file.write(f"{current_time} - {action}\n")  # Add datetime, action, and a newline

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

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # Visualize angle
            cv2.putText(image, str(angle), 
                            # replace 1280, 720 with camera feed resolution, finds location of elbow in actual feed
                           tuple(np.multiply(elbow, [1440, 980]).astype(int)), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            # action counter logic
            if angle > 160:
                stage = "prepare"
            if angle < 30 and stage =='prepare':
                stage="attack"
                counter +=1
                print(counter)

            # Instead of printing or just setting stage, write the action directly to the file
            if stage == "attack":
                write_action_to_file('01')
            elif stage == "prepare":
                write_action_to_file('00')  # Assuming you want to track this stage as well
            elif stage == "jumping":
                write_action_to_file('jump')
            # Add more elif blocks for other stages/actions as necessary
                
            current_left_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
            current_right_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
            if left_hip_y is not None and right_hip_y is not None:
                if (current_right_y - left_hip_y) >= threshold and (current_right_y - right_hip_y) >= threshold:            
                    cv2.putText(image, "jumping", 
                            # replace 1280, 720 with camera feed resolution,
                                (100,100), 
                           # fonts
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            left_hip_y = current_left_y
            right_hip_y = current_right_y


        except:
            pass

        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # data
        cv2.putText(image, 'Count', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, 'status', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

