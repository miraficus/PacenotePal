import os
import threading
import tkinter as tk
from tkinter import ttk

import yaml

from acrally import ACRally


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_frame = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

root = tk.Tk()
root.title("AC Rally Pacenote Pal editor")
root.geometry("600x600")
pacenote_elements = []
pacenote_vars = []

top_frame = ttk.Frame(root, padding=10)
top_frame.pack(fill="x")

pacenotes_combo = ttk.Combobox(top_frame, values=[x.replace(".yml", "") for x in os.listdir("pacenotes")])
voices_combo = ttk.Combobox(top_frame, values=[x for x in os.listdir("voices")])

pacenotes_combo.grid(row=0, column=0, padx=5, pady=5)
voices_combo.grid(row=0, column=1, padx=5, pady=5)

def load_pacenotes():
    global pacenote_elements, pacenote_vars
    [x.destroy() for x in pacenote_elements]
    pacenote_elements = []
    pacenote_vars = []

    acrally = ACRally(
        pacenotes_combo.get(),
        voices_combo.get(),
        1,
        None,
        None
    )
    token_sounds = acrally.build_token_sounds()

    pacenotes = yaml.safe_load(open(f"pacenotes/{pacenotes_combo.get()}.yml"))

    for i, pacenote in enumerate(pacenotes):
        playable_tokens = acrally.combine_tokens(pacenote["notes"], token_sounds)
        # print(pacenote["notes"], playable_tokens)

        def play(t=playable_tokens):
            threading.Thread(target=acrally.play_tokens, args=(t, token_sounds), daemon=True).start()
        play_btn = ttk.Button(scroll_frame.scrollable_frame, text="▶", width=3,
                         command=play)
        play_btn.grid(row=i, column=0, padx=5, pady=5)
        pacenote_elements.append(play_btn)

        distance_var = tk.StringVar(value=str(int(pacenote["distance"])))
        distance_lbl = ttk.Entry(scroll_frame.scrollable_frame, textvariable=distance_var, width=6)
        distance_lbl.grid(row=i, column=1, padx=5, pady=5)
        pacenote_elements.append(distance_lbl)
        pacenote_vars.append(distance_var)

        link_var = tk.BooleanVar(value=pacenote["link_to_next"])
        link_chk = ttk.Checkbutton(
            scroll_frame.scrollable_frame,
            variable=link_var,
            text="Link to next"
        )
        link_chk.grid(row=i, column=2, padx=5, pady=5)
        pacenote_elements.append(link_chk)
        pacenote_vars.append(link_var)

        pacenotes_frame = ttk.Frame(scroll_frame.scrollable_frame)
        pacenotes_frame.grid(row=i, column=3, padx=5, pady=5, sticky="w")
        for note_idx, t in enumerate(pacenote["notes"]):
            note_var = tk.StringVar(value=t)
            note_combo = ttk.Combobox(pacenotes_frame, values=list(token_sounds.keys()), textvariable=note_var)
            note_combo.grid(row=note_idx, column=0)
            note_up = ttk.Button(pacenotes_frame, text="↑", width=3)
            note_up.grid(row=note_idx, column=1)
            if note_idx == 0:
                note_up["state"] = "disabled"
            note_down = ttk.Button(pacenotes_frame, text="↓", width=3)
            note_down.grid(row=note_idx, column=2)
            if note_idx == len(pacenote["notes"]) - 1:
                note_down["state"] = "disabled"
            note_remove = ttk.Button(pacenotes_frame, text="🗑", width=3)
            note_remove.grid(row=note_idx, column=3)
            pacenote_vars.append(note_var)
        def add_note(i=i):
            pacenotes[i]["notes"].append("")
        add_button = ttk.Button(pacenotes_frame, text="Add +", command=add_note)
        add_button.grid(row=len(pacenote["notes"]), column=1, columnspan=3)
        pacenote_elements.append(pacenotes_frame)

        combined_pacenotes_frame = ttk.Frame(scroll_frame.scrollable_frame)
        combined_pacenotes_frame.grid(row=i, column=4, padx=5, pady=5, sticky="w")
        for t in playable_tokens:
            lbl = ttk.Label(combined_pacenotes_frame, text=t)
            lbl.pack(anchor="w")
            if pause := acrally.match_pause(t):
                lbl["text"] = f"Pause {pause} seconds"
                lbl["foreground"] = "blue"
            elif t not in token_sounds:
                lbl["foreground"] = "red"
        pacenote_elements.append(combined_pacenotes_frame)

load_button = ttk.Button(top_frame, text="Load", command=load_pacenotes)
load_button.grid(row=0, column=2, padx=10, pady=5)

# Scrollable frame
scroll_frame = ScrollableFrame(root)
scroll_frame.pack(fill="both", expand=True)


root.mainloop()
