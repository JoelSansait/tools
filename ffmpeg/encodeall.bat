@ECHO off
SETLOCAL

REM Similar to thpall, run this in a directory that has all the video folders

SET filetype=%1
SET targetdir=%2

FOR /f "tokens=*" %%i in ('DIR /a:d /b') DO (
	ffmpeg -r 30000/1001 -i .\%%i\%%i%%04d.%filetype% -vf scale=1920:1080 -c:v libx265 -crf 17 -r 30000/1001 -y %targetdir%\%%i.mp4
)
