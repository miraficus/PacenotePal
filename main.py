import os
import threading
import time
import tkinter as tk
from tkinter import ttk

import yaml

from acrally import ACRally


class Main:
    root = None
    stages = None
    voices = None
    call_earliness = None
    acrally = None
    btn_start = None
    btn_stop = None
    start_button = None


    def on_button_start(self):
        print(self.stages.get())
        self.acrally = ACRally(
            str(self.voices.get()),
            str(self.stages.get()),
            float(self.call_earliness.get()),
            self.start_button
        )
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"


    def on_button_exit(self):
        if self.acrally:
            self.acrally.exit()
        self.btn_start["state"] = "normal"
        self.btn_stop["state"] = "disabled"

    def on_button_distance(self):
        distance_window = tk.Toplevel(self.root)
        distance_window.title("Distance")
        distance_window.geometry("200x100")
        distance_window.attributes("-topmost", True)
        distance_var = tk.StringVar()
        distance_var.set("----")
        distance_label = ttk.Label(distance_window, textvariable=distance_var, font=("sans-serif", 40))
        distance_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        stop = False

        def retrieve_distance():
            nonlocal stop
            while not stop:
                if self.acrally:
                    if distance := self.acrally.get_distance():
                        distance_var.set(str(int(distance)))
                    else:
                        distance_var.set("----")
                time.sleep(0.05)

        def on_close():
            nonlocal stop
            stop = True
            distance_window.destroy()

        worker = threading.Thread(target=retrieve_distance, daemon=True)
        worker.start()
        distance_window.protocol("WM_DELETE_WINDOW", on_close)

    def __init__(self):
        config = yaml.safe_load(open("config.yml"))

        root = tk.Tk()
        root.title("AC Rally Pacenote Pal")
        root.geometry("340x360")
        self.root = root

        stages = os.listdir("pacenotes")
        stages = [file.replace(".yml", "") for file in stages]

        ttk.Label(root, text="Select a stage:").pack(pady=(20, 5))
        self.stages = ttk.Combobox(root, values=stages, width=50)
        self.stages.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        self.btn_start = ttk.Button(btn_frame, text="Start", command=self.on_button_start)
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = ttk.Button(btn_frame, text="Stop", command=self.on_button_exit, state="disabled")
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        self.btn_stop = ttk.Button(btn_frame, text="Distance", command=self.on_button_distance)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        self.start_button = config.get("start_button", "space")

        ttk.Label(root, text=f"Click start and press {self.start_button} when the countdown starts!").pack(pady=(20, 5))

        voices = os.listdir("voices")
        ttk.Label(root, text="Select a voice:").pack(pady=(20, 5))
        self.voices = ttk.Combobox(root, values=voices, width=50)
        self.voices.current(voices.index(config["voice"]))
        self.voices.pack(pady=5)

        ttk.Label(root, text="Call earliness multiplier (higher is earlier):").pack(pady=(20, 5))
        self.call_earliness = tk.Spinbox(
            root,
            from_=0.00,
            to=10.00,
            increment=0.01,
            textvariable=tk.DoubleVar(value=float(config["call_distance"])),
            format="%.2f",
            width=10
        )
        self.call_earliness.pack(padx=20, pady=20)

        root.mainloop()

if __name__ == '__main__':
    app = Main()
