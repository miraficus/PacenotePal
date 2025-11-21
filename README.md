AC Rally Pacenote Pal
=====================

Pacenote Pal is an application for Assetto Corsa Rally that replaces the in-game codriver with an external one.
This way you can use custom voices, edit the pacenotes per stage, and change the timing.

A demo can be found here: https://youtu.be/Quq5dFNgtvQ

**This software is nowhere near finished** and has many rough edges.

How it works
------------

1. Set the audio for the in-game spotter to 0%
2. Start the program
3. Select your stage
4. Press start 
5. Drive to the start of the stage. As the countdown starts, press the space bar. You will hear a beep

Adding a voice can be done by adding a folder in the folder `voices`. Changing the pacenotes can be done by 
editing the YAML files in the `pacenotes` folder, or adding a new file.

Thanks to
---------
pyaccsharedmemory.py is based on https://github.com/rrennoir/PyAccSharedMemory