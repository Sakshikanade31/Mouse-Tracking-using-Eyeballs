# Mouse-Tracking-using-Eyeballs
Control your mouse cursor using just your eyes and blinks — no hands needed! This project uses MediaPipe and FaceMesh to track eye landmarks and PyAutoGUI to move the mouse and simulate clicks.

# Purpose
This project aims to:
1. Enable hands-free mouse control for accessibility and convenience.
2. Provide left-click functionality via blink detection.
3. Serve as a base for gesture-based human-computer interaction systems.

# How It Works
1. MediaPipe FaceMesh detects 468 facial landmarks.
2. The iris movement is tracked to move the mouse pointer on screen.
3. Left eye blink is detected by measuring the distance between eyelid landmarks (145 & 159).
4. A calibration phase in the first few seconds determines your eye-open distance, improving accuracy.
5. Mouse movement is smoothed to reduce jitter.

# Requirements
1. Make sure you have Python 3.x installed, then run:
    pip install opencv-python mediapipe pyautogui
2. Download and Run the main Python script ie mouse_tracking_using_eyeball.py :
   python mouse_tracking_using_eyeball.py
3. Follow the instructions:
   a. Keep your eyes open during the first few seconds (for calibration).
   b. Move your eyes to control the cursor.
   c. Blink your left eye to perform a mouse click.

# Advantages
1. Accessible for users with physical disabilities.
2. Hardware-free — uses just your webcam.
3. Custom calibration adapts to each user.
4. Extensible — easily add gestures or voice commands.

# Future Improvements
1. Right-eye blink for right-click.
2. Eye-based scrolling or drag-and-drop.
3. Gesture-based UI for menu navigation.
4. On-screen overlay for gaze zones.
5. Voice or sound feedback.


  


