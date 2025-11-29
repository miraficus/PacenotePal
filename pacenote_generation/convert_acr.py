import os
import shutil


language = "French"
for language in ["Chinese", "English", "French", "German", "Italian", "Spanish"]:

    base = f'B:/Koen/Documents/Assetto Corsa Rally/Original pacenotes/{language}/Non Filtered'
    for file in os.listdir(base):
        if file.endswith("_Any_Any_1.wav"):
            clean_file = file.replace("PN_", "").replace("_Any_Any_1", "")
            clean_file = clean_file.replace("Uphill", "UpHill")
            shutil.copy2(f"{base}/{file}", f"../voices/{language}/{clean_file}")
            print(clean_file)

    print("Done.")
    print(set(os.listdir("../voices/Dutch")).difference(set(os.listdir(f"../voices/{language}"))))
    for file in set(os.listdir(f"../voices/{language}")).difference(set(os.listdir("../voices/Dutch"))):
        # os.remove(f"../voices/{language}/{file}")
        print(file)
