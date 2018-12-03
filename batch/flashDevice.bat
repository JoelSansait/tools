@echo off
setlocal enabledelayedexpansion
set PATH=%PATH%;C:\Users\jsansait\Documents\NVIDIA\scriptsAndTools\batch

REM ***********************************************************
REM Script to flash TV/Tablet and catch errors
REM Assumes that script and img files or IN THE SAME DIRECTORY
REM Written by jsansait@nvidia.com
REM ***********************************************************

SET dtbfile=0
REM SET currentFolder=%cd%

REM ***Check device connected***

fastboot devices | find "fastboot" >nul
if errorlevel 1 ( 
	echo No devices found. Ensure you are in bootloader and have drivers installed
	GOTO:theend
	)

REM *** Check that blob, boot, recovery, system, userdata, and vendor are all present ***
REM *** Warn the user if one of them is not present ***

REM *** Check if only one .dtb ***
REM *** If more than one, make the selection for the user ***

adb devices

REM FOR /F %%a in ('fastboot oem dtbname') do (
	REM dtbfile gets assigned to dtbfile                                          

	REM Some sample outputs
	
	REM ...
	REM (bootloader) Unknown Command!
	REM OKAY [  0.020s]
	REM finished. total time: 0.020s

	REM ...
	REM (bootloader) tegra210-foster-e-p2530-0930-e02-00.dtb  
	REM OKAY [  0.020s]
	REM finished. total time: 0.020s

	)

	REM At each command, make a yesno prompt IF a failure has been detected

	REM OKAY [  2.495s]
	REM sending sparse 'system' (65536 KB)...
	REM FAILED (remote: data too large)
	REM finished. total time: 93.358s

REM ***
REM fastboot oem dtbname
REM forloop that tokenizes output and grabs dtbname
REM fastboot flash staging blob
REM fastboot flash boot boot.img
REM fastboot flash recovery recovery.img
REM fastboot flash dtb %dtbname%
REM fastboot flash system system.img
REM fastboot flash userdata userdata.img
REM fastboot flash vendor vendor.img

REM If system is too big use this
REM fastboot flash -S 60M system system.img
REM ***


REM Error checking and handling
:theend
pause