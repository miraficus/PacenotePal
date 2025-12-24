import edge_tts
import asyncio
import os

VOICE_NAME = "cs-CZ-VlastaNeural"  # nebo cs-CZ-VlastaNeural, cs-CZ-AntoninNeural
OUTPUT_DIR = "voices/CzechVlastaTTS"
INPUT_FILE = "pacenotes-tts.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "=" not in line:
                continue

            key, text = line.strip().split("=", 1)
            outfile = os.path.join(OUTPUT_DIR, f"{key}.wav")

            print(f"Generating: {key} → {text}")

            tts = edge_tts.Communicate(text, VOICE_NAME)
            await tts.save(outfile)

asyncio.run(generate())

print("Done! All WAV files created")
