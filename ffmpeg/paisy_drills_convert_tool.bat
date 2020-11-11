@echo off

rem For converting all videos in a folder, for paisy drills

mkdir output
for /f "tokens=1 delims=." %%a in ('dir /B *.mp4') do ffmpeg -i "%%a.mp4" -c:v libx264 -vf scale=854:480 -crf 31 -an -preset veryslow ".\output\%%a.mp4"