import cv2
import numpy as np

# Output settings
width, height = 640, 480
fps = 30
frames = 100
outfile = "test.mp4"

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(outfile, fourcc, fps, (width, height))

if not writer.isOpened():
    raise RuntimeError("Failed to open VideoWriter")

# Define a palette of strong colors to cycle through
palette = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (255, 255, 255), # White
    (0, 0, 0)        # Black
]

for i in range(frames):
    # Pick a color (cycle through palette)
    color = palette[i % len(palette)]
    frame = np.full((height, width, 3), color, dtype=np.uint8)

    # Write the frame index number in the center
    text = str(i)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3
    thickness = 5

    # Get text size to center it
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2

    # Choose contrasting text color
    text_color = (0, 0, 0) if sum(color) > 400 else (255, 255, 255)

    cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, thickness, cv2.LINE_AA)

    writer.write(frame)

writer.release()
print(f"Wrote {frames} indexed frames to {outfile}")
