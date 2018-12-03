@echo off

REM ***Check device connected***

adb devices -l | find "device product:" >nul
if errorlevel 1 ( 
	echo No devices found 
	GOTO:thend
	)

adb shell screencap -p /sdcard/screencap.png
adb pull /sdcard/screencap.png  

:thend