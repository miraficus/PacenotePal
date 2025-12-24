import os
import subprocess

VOICE_NAME = "cs-CZ-AntoninNeural"  # nebo cs-CZ-VlastaNeural, cs-CZ-AntoninNeural
OUTPUT_DIR = "voices/CzechAntoninTTS"
INPUT_FILE = "pacenotes-tts.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if "=" not in line:
            continue

        key, text = line.strip().split("=", 1)

        mp3_file = os.path.join(OUTPUT_DIR, f"{key}.mp3")
        wav_file = os.path.join(OUTPUT_DIR, f"{key}.wav")

        print(f"Generating: {key} → {text}")

        # 1) Vygenerovat MP3 přes edge-tts
        cmd_tts = [
            "py", "-3.11", "-m", "edge_tts",
            "--voice", VOICE_NAME,
            "--text", text,
            "--write-media", mp3_file
        ]
        subprocess.run(cmd_tts, check=True)

        # 2) Převést MP3 → WAV (PCM 16bit mono 22050 Hz)
        cmd_ffmpeg = [
            "ffmpeg", "-y",
            "-i", mp3_file,
            "-ac", "1",
            "-ar", "22050",
            "-sample_fmt", "s16",
            wav_file
        ]
        subprocess.run(cmd_ffmpeg, check=True)

        # 3) Smazat MP3 (není potřeba)
        os.remove(mp3_file)

print("Hotovo! WAV soubory jsou skutečné PCM WAV a kompatibilní s PacenotePal.")

