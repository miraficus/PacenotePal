import json
import os.path
import random
import re
import time
from threading import Thread

import keyboard
import winsound

from pyaccsharedmemory import accSharedMemory


call_earliness = 120

stages = os.listdir("pacenotes")
for i, file in enumerate(stages):
    print(f"[{i + 1}] {file.replace(".json", "")}")
stage_no = input("Enter the number of the stage: ")
stage = stages[int(stage_no) - 1]
# stage = "DT_PacenoteHafrenNorthFullReverse"
notes = json.load(open(f"pacenotes/{stage}"))[0]["Rows"]
notes_list = []
for k, v in notes.items():
    notes_list.append(v)

exit_all = False
started = False
last_retrieve = time.time()
speed_kmh = 0
# Distance does not always start at 0
distance = notes_list[0]["SplineDistanceM"]

def retrieve_thread():
    global distance, last_retrieve, exit_all, started, speed_kmh

    asm = accSharedMemory()
    last_shared_memory = None

    print("Press the space bar when the countdown starts!")
    while not keyboard.is_pressed("space"):
        time.sleep(0.1)
    winsound.Beep(800, 250)

    while not exit_all:
        sm = asm.read_shared_memory()
        if sm is None:
            sm = last_shared_memory

        if sm is not None:
            now = time.time()
            delta_t = now - last_retrieve
            last_retrieve = now
            speed_kmh = sm.Physics.speed_kmh
            speed_ms = speed_kmh * (5/18)
            distance += speed_ms * delta_t

            if speed_ms > 5:
                # Detect whether player has set off from start line
                started = True

            # print(distance, sm.Static.track_length)
            last_shared_memory = sm
        else:
            # print(None)
            continue
        time.sleep(0.05)

    asm.close()

def speak_thread():
    global distance, notes_list, call_earliness, exit_all, started, speed_kmh

    # engine = pyttsx3.init()
    # initial_distance = distance
    # while distance - initial_distance < 170:
    #     # Do not immediately blurt out everything before the start of the stage
    #     time.sleep(0.1)

    while not exit_all and not started:
        time.sleep(0.1)

    while len(notes_list) > 0 and not exit_all:
        if notes_list[0]["SplineDistanceM"] < distance + call_earliness + (speed_kmh // 2):
            note = notes_list.pop(0)
            tokens = note["TokenList"]["Tokens"]
            # print(tokens)
            link_to_next = note["LinkToNext"]
            while link_to_next:
                next_note = notes_list.pop(0)
                next_tokens = next_note["TokenList"]["Tokens"]
                tokens.extend(next_tokens)
                link_to_next = next_note["LinkToNext"]

            for token in tokens:
                print(token)
                if matches := re.match('Pause([\\d.]+)s(?:_Reset)?', token):
                    pause_time = float(matches.group(1))
                    print(f"Sleeping for {pause_time}")
                    time.sleep(pause_time)
                else:
                    files = [entry for entry in os.listdir("voices") if entry.startswith(token)]
                    if len(files) > 0:
                        filename = f"voices\\{random.choice(files)}"
                        winsound.PlaySound(filename, winsound.SND_FILENAME)
                # engine.say(token)
            # engine.runAndWait()
        else:
            time.sleep(0.1)

retrieve = Thread(target=retrieve_thread, daemon=True)
speak = Thread(target=speak_thread, daemon=True)
retrieve.start()
speak.start()
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    exit(0)
