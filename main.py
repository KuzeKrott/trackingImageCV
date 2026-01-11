import cv2
import numpy as np
import ctypes
from comPortFind import ComPortApp
import tkinter as tk

root = tk.Tk()
app = ComPortApp(root)

ctypes.windll.user32.ShowCursor(False)
mouse_x, mouse_y = 0, 0
figureSize = 50
video_capture = cv2.VideoCapture(0)

# def coord_listener(x, y):
#     print(f"[Listener] Current coordinates: X={x}, Y={y}")

#callback
def on_mouse(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y
        

win_name = "Mouse Tracker"
cv2.namedWindow(win_name)
cv2.setMouseCallback(win_name, on_mouse)

half = figureSize//2
while True:
    result, display = video_capture.read()  # read frames from the video
    cv2.rectangle(display, 
                  (mouse_x - half, mouse_y - half), 
                  (mouse_x + half, mouse_y + half), 
                  (255, 0, 0), 
                  5)

    cv2.putText(display, f"Coordinate: X={mouse_x}, Y={mouse_y}", (10, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (23, 187, 76), 2)
    cv2.imshow(win_name, display)

    if cv2.waitKey(20) & 0xFF == 27: 
        # app.send_read_test_message("G1 X10 Y20")
        break

ctypes.windll.user32.ShowCursor(True)
video_capture.release()
cv2.destroyAllWindows()