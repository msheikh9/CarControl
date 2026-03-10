
import cv2
import mediapipe as mp
import time
import math

def dist(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def lm_xy(hand_landmarks, idx, w, h):
    lm = hand_landmarks.landmark[idx]
    return (lm.x * w, lm.y * h)

def thumb_direction(hand_landmarks, w, h):
    WRIST = mp.solutions.hands.HandLandmark.WRIST
    THUMB_MCP = mp.solutions.hands.HandLandmark.THUMB_MCP
    THUMB_TIP = mp.solutions.hands.HandLandmark.THUMB_TIP
    MIDDLE_MCP = mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP

    wrist = lm_xy(hand_landmarks, WRIST, w, h)
    middle_mcp = lm_xy(hand_landmarks, MIDDLE_MCP, w, h)
    hand_scale = dist(wrist, middle_mcp) + 1e-6

    mcp = lm_xy(hand_landmarks, THUMB_MCP, w, h)
    tip = lm_xy(hand_landmarks, THUMB_TIP, w, h)

    extended = dist(tip, mcp) > 0.35 * hand_scale
    dy = tip[1] - mcp[1]
    margin = 0.10 * hand_scale

    if extended and dy < -margin:
        return "up"
    elif extended and dy > margin:
        return "down"
    else:
        return "neutral"

def pointing_gesture_vertical(hand_landmarks):
    idx = mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP
    th  = mp.solutions.hands.HandLandmark.THUMB_TIP
    index_y = hand_landmarks.landmark[idx].y
    thumb_y = hand_landmarks.landmark[th].y
    eps = 0.03
    if index_y < thumb_y - eps:
        return "pointing up"
    elif index_y > thumb_y + eps:
        return "pointing down"
    else:
        return "other"

def pointing_gesture_horizontal(hand_landmarks):
    idx = mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP
    th  = mp.solutions.hands.HandLandmark.THUMB_TIP
    index_x = hand_landmarks.landmark[idx].x
    thumb_x = hand_landmarks.landmark[th].x
    eps = 0.04
    if index_x > thumb_x + eps:
        return "pointing right"
    elif index_x < thumb_x - eps:
        return "pointing left"
    else:
        return "other"


state = "idle"
car_volume = 50
last_vol_time = 0.0
vol_cooldown = 0.5
last_call_time = 0.0
call_cooldown = 0.8
tracks = ["Song A", "Song B", "Song C", "Song D"]
current_track = 0
last_track_time = 0.0
track_cooldown = 0.8


def open_camera(preferred_indices=(1,0)):
    for i in preferred_indices:
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Opened camera index {i}")
            return cap, i
        else:
            cap.release()
    return None, None

cap, used_index = open_camera((1,0))
if cap is None:
    raise SystemExit("ERROR: Could not open any camera. Try checking camera permissions or using a different index.")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame read failed — stopping.")
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        gesture_text = "none"

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if state != "ringing":
                g_v = pointing_gesture_vertical(hand_landmarks)
                gesture_text = g_v
                now = time.time()
                if now - last_vol_time > vol_cooldown:
                    if g_v == "pointing up" and car_volume < 100:
                        car_volume += 5
                        last_vol_time = now
                    elif g_v == "pointing down" and car_volume > 0:
                        car_volume -= 5
                        last_vol_time = now

            if state != "ringing":
                g_h = pointing_gesture_horizontal(hand_landmarks)
                if g_h != "other":
                    gesture_text = g_h
                now = time.time()
                if now - last_track_time > track_cooldown:
                    if g_h == "pointing right":
                        current_track = (current_track + 1) % len(tracks)
                        last_track_time = now
                    elif g_h == "pointing left":
                        current_track = (current_track - 1) % len(tracks)
                        last_track_time = now

            td = thumb_direction(hand_landmarks, w, h)
            if state == "ringing":
                if td in ("up", "down"):
                    gesture_text = f"thumb {td}"
                now = time.time()
                if now - last_call_time > call_cooldown:
                    if td == "up":
                        state = "in_call"
                        last_call_time = now
                    elif td == "down":
                        state = "idle"
                        last_call_time = now
            elif state == "in_call":
                if td == "down":
                    now = time.time()
                    if now - last_call_time > call_cooldown:
                        state = "idle"
                        last_call_time = now

        cv2.rectangle(frame, (40, 100), (70, 400), (255, 255, 255), 2)
        vol_h = int((car_volume / 100.0) * 300)
        cv2.rectangle(frame, (40, 400 - vol_h), (70, 400), (0, 200, 0), -1)
        cv2.putText(frame, f"Car Volume: {car_volume}%", (90, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        cv2.putText(frame, f"Track: {tracks[current_track]}", (90, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 220, 0), 2)
        cv2.putText(frame, f"Gesture: {gesture_text}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 220, 0), 2)

        if state == "idle":
            cv2.putText(frame, "Press 'C' to simulate incoming call",
                        (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        elif state == "ringing":
            cv2.rectangle(frame, (110, 60), (w-110, 130), (0, 200, 255), -1)
            cv2.putText(frame, "Incoming Call...  (Thumb UP = Accept, Thumb DOWN = Reject)",
                        (130, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (20, 20, 20), 2)
        elif state == "in_call":
            cv2.rectangle(frame, (140, 60), (w-140, 130), (0, 180, 0), -1)
            cv2.putText(frame, "In Call  (Thumb DOWN = End)", (w//2 - 180, 105),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("Gesture Car Control (Volume + Call + Music)", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key in (ord('c'), ord('C')):
            if state != "in_call":
                state = "ringing"

finally:
    if 'cap' in locals() and cap is not None:
        cap.release()
    cv2.destroyAllWindows()
