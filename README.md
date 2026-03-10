Car Control System
Real-Time Hand Gesture Interface using OpenCV & MediaPipe

Overview

This project is a real-time hand gesture recognition system that simulates car-style controls using a webcam. It uses MediaPipe Hands for landmark detection and OpenCV for video processing and UI rendering.

The system allows users to control volume, switch music tracks, and manage calls using simple hand gestures. All interactions are touch-free and processed live from the camera feed.

Features

Real-time hand tracking (single hand)

Gesture-based volume control

Gesture-based music track navigation

Simulated incoming call handling

On-screen UI with volume bar and status display

Cooldown protection to prevent repeated gesture triggers

Automatic camera fallback (tries multiple camera indices)

Technologies Used

Python 3.8+

OpenCV

MediaPipe Hands

Standard Python libraries (math, time)

Installation

Create a virtual environment (recommended)

Install required packages:

pip install opencv-python mediapipe

Running the Application

Save the script as:

gesture_car_control.py

Run:

python gesture_car_control.py

Press:

Q → Quit

C → Simulate incoming call

Gesture Controls
Volume Control

(Disabled while phone is ringing)

Pointing Up → Increase volume by 5%

Pointing Down → Decrease volume by 5%

Detection compares the vertical position of the index fingertip relative to the thumb tip.

Cooldown: 0.5 seconds

Music Control

(Disabled while phone is ringing)

Pointing Right → Next track

Pointing Left → Previous track

Detection compares the horizontal position of the index fingertip relative to the thumb tip.

Cooldown: 0.8 seconds

Tracks cycle through:

["Song A", "Song B", "Song C", "Song D"]

Call Handling

Press C to simulate an incoming call.

While Ringing:

Thumb Up → Accept call

Thumb Down → Reject call

While In Call:

Thumb Down → End call

Thumb detection is based on:

Hand scale (distance between wrist and middle finger MCP)

Thumb extension length

Vertical offset between thumb MCP and thumb tip

Cooldown: 0.8 seconds

System States

The application uses a simple state machine:

idle → ringing → in_call → idle

UI Elements

Volume bar (0–100%)

Current track display

Detected gesture label

Call status banner

Instruction text for call simulation

Camera Handling

The program attempts to open camera indices in this order:

(1, 0)

If your camera does not open, modify:

open_camera((1,0))

to try other indices such as:

open_camera((0,1,2))

Customization

You can adjust:

Volume cooldown:
vol_cooldown = 0.5

Track cooldown:
track_cooldown = 0.8

Call cooldown:
call_cooldown = 0.8

Gesture sensitivity:
Vertical epsilon = 0.03
Horizontal epsilon = 0.04
Thumb extension threshold = 0.35 * hand_scale
Thumb direction margin = 0.10 * hand_scale

Limitations

Supports one hand only

Works best with good lighting

Gesture detection is heuristic-based and may vary with hand orientation

This is a simulation only — no real vehicle or audio system integration

Project Structure
├── gesture_car_control.py
└── README.md
