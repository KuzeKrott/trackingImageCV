import cv2
import numpy as np
import ctypes

ctypes.windll.user32.ShowCursor(False) # делаем курсор невидимым 
mouse_x, mouse_y = 0, 0
figureSize = 50
video_capture = cv2.VideoCapture(0)

#callback
def on_mouse(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

img = np.zeros((600, 800, 3), dtype=np.uint8)
win_name = "Mouse Tracker"
cv2.namedWindow(win_name)

cv2.setMouseCallback(win_name, on_mouse) # функция из OpenCV, передаётся ссылка на ф-цию on_mouse

half = figureSize//2
while True:
    result, display = video_capture.read()  # read frames from the video
    cv2.rectangle(display, 
                  (mouse_x - half, mouse_y - half), 
                  (mouse_x + half, mouse_y + half), 
                  (255, 0, 0), 
                  5)

    cv2.imshow(win_name, display)

    if cv2.waitKey(20) & 0xFF == 27: 
        break

ctypes.windll.user32.ShowCursor(True)
video_capture.release()
cv2.destroyAllWindows()