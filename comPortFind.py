from tkinter import *
from tkinter import ttk
import serial.tools.list_ports

root = Tk()
root.title("Mouse Tracker")
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
windowPosX = screenWidth // 2 - 400
windowPosY = screenHeight // 2 - 300
root.geometry(f"800x600+{windowPosX}+{windowPosY}")
frm = ttk.Frame(root, padding=20)
frm.grid()

def on_select(event):
    print("Выбрано:", combo.get())
options = []



combo = ttk.Combobox(frm, values=options)
combo.grid(column=1, row=0)
combo.current(0)
combo.bind("<<ComboboxSelected>>", on_select)

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device, port.description, port.hwid)

Label(
    frm, 
    text="Choose source port"
).grid(column=0, row=0)
Label(
    frm, 
    text="Choose destination port"
).grid(column=0, row=1)
Button(
    frm,
    text="test",
    width=10,
    height=2,
).grid(column=4, row=0, padx=2, pady=1)

#ttk.Label(frm, text = "Hello World!").grid(column = 0, row = 0)
Button(
    frm, 
    text = "Quit", 
    width=10,
    height=2,
    command = root.destroy
).grid(column = 4, row = 1, padx=2, pady=1)

root.mainloop()
