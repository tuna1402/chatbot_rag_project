import cv2
import mediapipe as mp
import os

def process_video(input_path, output_path, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    # Initialize MediaPipe Hands and drawing utilities
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=max_num_hands, 
                           min_detection_confidence=min_detection_confidence, 
                           min_tracking_confidence=min_tracking_confidence)
    mp_drawing = mp.solutions.drawing_utils

    # Capture video from the input path
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    # Define the codec and create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb_frame)

        # Draw hand landmarks on the frame
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        out.write(frame)  # Write the frame with landmarks to the output video

        frame_count += 1
        print(f"Processing frame {frame_count}", end='\r')

        # Display the frame for visualization (optional)
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"\nProcessing complete. Output saved to {output_path}")

# Example usage:
input_video_path = "videos/ccc.mp4"
output_video_path = "videos/output_tracked.avi"

# Create the output directory if it doesn't exist
output_dir = os.path.dirname(output_video_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

process_video(input_video_path, output_video_path)
