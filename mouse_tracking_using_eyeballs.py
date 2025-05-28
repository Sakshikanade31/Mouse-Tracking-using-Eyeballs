import cv2
import mediapipe as mp
import pyautogui
import time

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Mouse smoothing
prev_x, prev_y = screen_w / 2, screen_h / 2
smoothing_factor = 0.2

# Click delay control
last_click_time = 0
click_delay = 2  # seconds

# Calibration
calibrating = True
calibration_frames = 100
eye_open_distances = []

blink_threshold_ratio = 0.25  # Blink = 25% or less of open eye distance
calibrated_threshold = None

frame_count = 0

print("Please keep your eyes open for calibration...")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Get iris coordinates and move cursor
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if id == 1:
                target_x = screen_w * landmark.x
                target_y = screen_h * landmark.y
                curr_x = prev_x + (target_x - prev_x) * smoothing_factor
                curr_y = prev_y + (target_y - prev_y) * smoothing_factor
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

        # Detect blink using landmarks 145 (upper eyelid) and 159 (lower eyelid)
        left_eye_top = landmarks[145]
        left_eye_bottom = landmarks[159]

        # Draw eye points
        x1 = int(left_eye_top.x * frame_w)
        y1 = int(left_eye_top.y * frame_h)
        x2 = int(left_eye_bottom.x * frame_w)
        y2 = int(left_eye_bottom.y * frame_h)
        cv2.circle(frame, (x1, y1), 3, (0, 255, 255))
        cv2.circle(frame, (x2, y2), 3, (0, 255, 255))

        eye_distance = abs(left_eye_top.y - left_eye_bottom.y)

        if calibrating:
            eye_open_distances.append(eye_distance)
            frame_count += 1
            if frame_count >= calibration_frames:
                avg_open_distance = sum(eye_open_distances) / len(eye_open_distances)
                calibrated_threshold = avg_open_distance * blink_threshold_ratio
                calibrating = False
                print(f"Calibration done. Blink threshold set to: {calibrated_threshold:.5f}")
        else:
            if eye_distance < calibrated_threshold:
                current_time = time.time()
                if current_time - last_click_time > click_delay:
                    pyautogui.click()
                    last_click_time = current_time
                    print('mouse clicked')

    # Display frame
    cv2.imshow("EYEBALL MOUSE TRACKING + CALIBRATED BLINK", frame)

    key = cv2.waitKey(10)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
