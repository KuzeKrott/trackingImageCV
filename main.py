import ctypes
import tkinter as tk
from tkinter import ttk

import cv2
from PIL import Image, ImageTk


class MouseTrackerApp:
    def __init__(self, root: tk.Tk, camera_index: int = 0, figure_size: int = 50) -> None:
        self.root = root
        self.cap = cv2.VideoCapture(camera_index)

        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Camera error")

        self.h, self.w = frame.shape[:2]
        self.half = figure_size // 2

        self.mouse_x = 0
        self.mouse_y = 0
        self.running = True

        self.canvas = tk.Canvas(root, width=self.w, height=self.h, highlightthickness=0)
        self.label = ttk.Label(root, text="Coordinate: X=0, Y=0")

        self.canvas.pack()
        self.label.pack(pady=6)

        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Enter>", self._hide_cursor)
        self.canvas.bind("<Leave>", self._show_cursor)

        self.root.protocol("WM_DELETE_WINDOW", self._close)

        self._update_frame()

    # -------------------------------------------------------------

    def _hide_cursor(self, _event=None) -> None:
        ctypes.windll.user32.ShowCursor(False)

    def _show_cursor(self, _event=None) -> None:
        ctypes.windll.user32.ShowCursor(True)

    def _on_mouse_move(self, event: tk.Event) -> None:
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.label.config(text=f"Coordinate: X={self.mouse_x}, Y={self.mouse_y}")

    # -------------------------------------------------------------

    def _update_frame(self) -> None:
        if not self.running:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.root.after(20, self._update_frame)
            return

        cv2.rectangle(
            frame,
            (self.mouse_x - self.half, self.mouse_y - self.half),
            (self.mouse_x + self.half, self.mouse_y + self.half),
            (255, 0, 0),
            2,
        )

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(Image.fromarray(frame))

        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(20, self._update_frame)

    # -------------------------------------------------------------

    def _close(self) -> None:
        self.running = False
        self.cap.release()
        self._show_cursor()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    MouseTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
