import cv2
import mediapipe as mp
import os

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

prev_frame_time = 0
new_frame_time = 0

# Video capture object
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 40)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Adjust as needed
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Adjust as needed
recording = False
out = None

output_dir = "videos"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_path = os.path.join(output_dir, "output.avi")

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if recording:
        out.write(frame)
        frame_count += 1
        print(f"Recording frame {frame_count}", end='\r')

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and detect hands
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Calculate FPS
    time_diff = new_frame_time - prev_frame_time
    if time_diff > 0:  # Avoid division by zero
        fps = 1 / time_diff
    else:
        fps = 0
        
    prev_frame_time = new_frame_time
    fps = int(fps)
          
    cv2.putText(frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Frame', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):
        print(recording)
        if not recording:
            recording = True
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path, fourcc, 50.0, (frame.shape[1], frame.shape[0]))
            print("Recording started")
    elif key == ord('a'):  # F10 key stops recording (F10 keycode is 0x79)
        if recording:
            recording = False
            out.release()
            print("Recording stopped")

    if recording:
        out.write(frame)

cap.release()
cv2.destroyAllWindows()
