# Hand Gesture-Controlled Slide Navigation

This project enables gesture-based slide navigation using OpenCV, MediaPipe, and DirectX key simulation. The system detects hand gestures via a webcam and maps them to keyboard inputs for navigating slides.

## Features
- **Hand Gesture Recognition**: Uses MediaPipe Hands to detect and track hand movements.
- **Gesture-Based Slide Navigation**:
  - Closed fist → Next Slide
  - Open palm → Next Slide
  - Two fingers (index and middle) extended → Previous Slide
- **Keyboard Emulation**: Simulates keyboard presses for slide transitions.
- **Real-Time Processing**: Runs efficiently using OpenCV and MediaPipe for hand tracking.

## Requirements
- Python 3.7+
- OpenCV
- MediaPipe
- `directkeys.py` (for simulating keyboard input)

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/gesture-slide-control.git
   cd gesture-slide-control
   ```
2. Install dependencies:
   ```sh
   pip install opencv-python mediapipe
   ```
3. Ensure `directkeys.py` is available in the working directory.

## Usage
Run the script with:
```sh
python hand_gesture_control.py
```

### Hand Gestures
- **Closed Fist** → Move to the next slide.
- **Open Palm** → Move to the next slide.
- **Two Fingers Up (Index + Middle)** → Move to the previous slide.

- Ensure your webcam is connected.
- Use hand gestures to navigate slides.
- Press `q` to exit.

## File Overview
- `hand_gesture_control.py` → Main script for hand gesture recognition and slide navigation.
- `directkeys.py` → Utility script for simulating keyboard inputs.

## Troubleshooting
- If the script doesn't detect gestures properly, adjust the `min_detection_confidence` and `min_tracking_confidence` values.
- Ensure no other applications are using the webcam.
- If keyboard emulation fails, run the script with administrator privileges.

## License
This project is licensed under the MIT License.

## Author
[Your Name] - [Your GitHub Profile]

