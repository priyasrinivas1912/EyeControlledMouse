# EyeControlledMouse

The Eye-Controlled Mouse Project is an innovative system that enables hands-free computer interaction by tracking users' eye movements and translating them into cursor actions. Utilizing computer vision and eye-tracking technology, the system detects facial landmarks, monitors eye movement, and maps gaze positions to screen coordinates. Additionally, it incorporates blink detection or gaze-dwell techniques for performing mouse clicks. The project leverages OpenCV for real-time image processing, MediaPipe for facial landmark detection, and PyAutoGUI for GUI automation, ensuring seamless and efficient operation.

🔍 Current (Existing) Eye-Controlled Mouse Systems: An Overview
1. Core Components

Most systems follow this block architecture:

+---------------------+
|     Webcam Input    |
+----------+----------+
           |
+----------v----------+
| Frame Preprocessing |
+----------+----------+
           |
   +-------v--------+
   | Eye/Face Tracker|
   +-------+--------+
           |
   +-------v--------+
   | Gaze Estimation |
   +-------+--------+
           |
   +-------v--------+
   | Cursor Control  |
   +-----------------+

🧠 How It Works (Technically)

Step 1: Camera Initialization

“We begin by activating the webcam to capture live facial video.
Each frame is instantly processed to detect a face—this forms the foundation of our system’s real-time responsiveness.”

Step 2: Face & Eye Landmark Detection

“Next, using MediaPipe Face Mesh, a cutting-edge AI framework, we detect precise landmarks on the face and eyes.
These key points are like a digital map of your eye movements—this is where innovation happens, because we convert raw video into actionable signals.”

Step 3: Eye Movement Tracking

“Finally, we extract the pupil coordinates to detect exactly where you’re looking and translate that into on-screen cursor movement.
This means your gaze becomes a powerful input device.”

Step 4: Cursor Movement Execution

“After detecting where the user is looking, we use PyAutoGUI, a powerful Python automation library, to actually move the mouse pointer.
So when the system detects your gaze shifting left, right, up, or down—your cursor follows seamlessly in real time.
This is the moment the eyes truly become the mouse.”

⚡ Step 5: Blink Detection for Clicks

“We needed a natural way to click without using hands.
So, we designed a mechanism to detect intentional blinks using threshold values.
A blink is no longer just a reflex—it becomes a command. A blink triggers a click.
This unlocks hands-free control for people with mobility limitations or scenarios where touch is impractical.”
🧰 Tools and Libraries Commonly Used

OpenCV – For camera I/O and image processing.

Dlib / Mediapipe – For face and landmark detection.

PyAutoGUI / pynput – To control the mouse.
