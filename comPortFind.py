import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

class ComPortApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Mouse Tracker")

        # ---- состояние ----
        self.selected_src_com = ""
        self.selected_dst_com = ""

        # ---- геометрия положения окна ----
        self._setup_geometry()

        # ---- интерфейс ----
        self._create_widgets()

        # ---- загрузка COM-портов ----
        self._load_com_ports()

    # ------------------------
    # Настройка окна
    # ------------------------
    def _setup_geometry(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w // 2 - 400
        y = screen_h // 2 - 300
        self.root.geometry(f"800x600+{x}+{y}")

    # ------------------------
    # Создание виджетов
    # ------------------------
    def _create_widgets(self):
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.grid()

        # Метки
        ttk.Label(self.frame, text="Choose source port").grid(column=0, row=0, sticky="w")
        #ttk.Label(self.frame, text="Choose destination port").grid(column=0, row=1, sticky="w")

        # Combobox src
        self.src_combo = ttk.Combobox(self.frame, values=[])
        self.src_combo.grid(column=1, row=0)
        self.src_combo.bind("<<ComboboxSelected>>", self.on_select_src)

        # # Combobox dst
        # self.dst_combo = ttk.Combobox(self.frame, values=[])
        # self.dst_combo.grid(column=1, row=1)
        # self.dst_combo.bind("<<ComboboxSelected>>", self.on_select_dst)

        # окно вывода сообщений
        self.log = tk.Text(self.frame, width=60, height=10)
        self.log.grid(column=0, row=3, columnspan=4)

        # Кнопки
        ttk.Button(
            self.frame,
            text="Quit",
            width=20,
            command=self.root.destroy
        ).grid(column=1, row=10, padx=2, pady=1)

        ttk.Button(
            self.frame,
            text="send&read",
            width=16,
            command=self.send_read_test_message
        ).grid(column=1, row=4, padx=2, pady=1)

    # ------------------------
    # Логика
    # ------------------------
    def _load_com_ports(self):
        ports = serial.tools.list_ports.comports()
        com_ports = [p.device for p in ports]

        self.src_combo["values"] = com_ports
        #self.dst_combo["values"] = com_ports

        if com_ports:
            self.src_combo.current(0)
            #self.dst_combo.current(0)
            self.selected_src_com = com_ports[0]
            self.selected_dst_com = com_ports[0]

    def on_select_src(self, event=None):
        self.selected_src_com = self.src_combo.get()
        print("Selected src:", self.selected_src_com)

    # def on_select_dst(self, event=None):
    #     self.selected_dst_com = self.dst_combo.get()
    #     print("Selected dst:", self.selected_dst_com)

    def log_message(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def open_port(self):
        try:
            self.serial = serial.Serial(
                port=self.selected_src_com,
                baudrate=9600,
                timeout=1
            )
            print("Port opened:", self.selected_src_com)
        except Exception as e:
            print("Error opening port:", e)

    def close_port(self):
        if hasattr(self, "serial") and self.serial.is_open:
            self.serial.close()
            print("Port closed")

    def read_from_port(self):
        if not hasattr(self, "serial") or not self.serial.is_open:
            print("Port not opened")
            return
        try:
            data = self.serial.readline()
            if data:
                text = data.decode("utf-8", errors="ignore").strip()
                print("Received:", text)
                self.log_message(f"Received: {text}")
        except Exception as e:
            print("Read error:", e)

    def send_read_test_message(self):
        self.open_port()
        if not hasattr(self, "serial") or not self.serial.is_open:
            print("Port not opened")
            return

        self.serial.write(b"HELLO FROM PYTHON\n")
        print("Sent test message")
        self.read_from_port()
        self.close_port()

# ------------------------
# Точка входа
# ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ComPortApp(root)
    root.mainloop()
