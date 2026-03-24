# Gesture Car Control

Real-time hand gesture interface for car-style controls — volume, music, and calls — using OpenCV and MediaPipe. No touch required.

---

## Requirements

- Python 3.8+
- `opencv-python`
- `mediapipe`
```bash
pip install opencv-python mediapipe
```

---

## Usage
```bash
python gesture_car_control.py
```

| Key | Action |
|-----|--------|
| `Q` | Quit |
| `C` | Simulate incoming call |

---

## Gesture Reference

> Volume and track controls are **disabled while the phone is ringing.**

### Volume — index finger vs. thumb tip (vertical, ε = 0.03)
| Gesture | Action |
|---------|--------|
| Index above thumb | +5% volume |
| Index below thumb | −5% volume |

Cooldown: 0.5s

### Music — index finger vs. thumb tip (horizontal, ε = 0.04)
| Gesture | Action |
|---------|--------|
| Index right of thumb | Next track |
| Index left of thumb | Previous track |

Cooldown: 0.8s · Tracks cycle: `["Song A", "Song B", "Song C", "Song D"]`

### Calls — thumb direction (extension threshold: 0.35× hand scale)
| State | Gesture | Action |
|-------|---------|--------|
| Ringing | Thumb up | Accept |
| Ringing | Thumb down | Reject |
| In call | Thumb down | End call |

Cooldown: 0.8s

---

## State Machine
```
idle → ringing → in_call → idle
```

---

## Camera Troubleshooting

The app tries camera indices `(1, 0)` by default. If your camera isn't detected, edit `open_camera(...)`:
```python
open_camera((0, 1, 2))
```

---

## Tuning

| Parameter | Variable | Default |
|-----------|----------|---------|
| Volume cooldown | `vol_cooldown` | `0.5` |
| Track cooldown | `track_cooldown` | `0.8` |
| Call cooldown | `call_cooldown` | `0.8` |
| Vertical sensitivity | `eps` in `pointing_gesture_vertical` | `0.03` |
| Horizontal sensitivity | `eps` in `pointing_gesture_horizontal` | `0.04` |
| Thumb extension | threshold in `thumb_direction` | `0.35 × hand_scale` |

---

## Limitations

- Single hand only
- Heuristic-based detection — performance varies with lighting and hand orientation
- Simulation only — no real vehicle or audio system integration

---

## Project Structure
```
├── gesture_car_control.py
└── README.md
```
