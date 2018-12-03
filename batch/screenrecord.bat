@ECHO off

adb shell screenrecord /sdcard/vid.mp4
pause
adb pull /sdcard/vid.mp4 
