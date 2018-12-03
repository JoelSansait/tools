@ECHO off
SETLOCAL

set lqdir=%1
set hqdir=%2
set targetdir=%3

FOR /f "tokens=*" %%i in ('DIR /a:d /b') DO (
    ffmpeg -r 30000/1001 -i %lqdir%\%%i.mp4 -r 30000/1001 -i %hqdir%\%%i.mp4 -filter_complex "[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[vid]" -map [vid] -c:v libx264 -crf 17 -r 30000/1001 -an -y %targetdir%\%%i_comparison.mp4
)