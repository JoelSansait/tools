@ECHO off
SETLOCAL

REM Run this in folder with all the SMS jpegs

SET targetdir=%1

FOR /f "tokens=*" %%i in ('DIR /a:d /b') DO (
	ffmpeg -r 30000/1001 -i .\%%i\%%i%%04d.jpg -vf scale=1920:1080:flags=neighbor -c:v libx264 -crf 17 -r 30000/1001 -y %targetdir%\%%i.mp4
)
