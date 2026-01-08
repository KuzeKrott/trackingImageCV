import cv2
import numpy as np

mouse_x, mouse_y = -1, -1

#callback
def on_mouse(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y
        print(f"Mouse moved to: ({mouse_x}, {mouse_y})")

# создаем пустое изображение
img = np.zeros((600, 800, 3), dtype=np.uint8)

# задаем имя окна
win_name = "Mouse Tracker"
cv2.namedWindow(win_name)

# регистрируем callback
cv2.setMouseCallback(win_name, on_mouse)

print("Move mouse inside the window...")
while True:
    display = img.copy()
    cv2.putText(display, f"X: {mouse_x}, Y: {mouse_y}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow(win_name, display)
    if cv2.waitKey(20) & 0xFF == 27:  # выход по ESC
        break

cv2.destroyAllWindows()