@ECHO off
SETLOCAL enabledelayedexpansion
SET PATH=%PATH%;C:\Users\jsansait\Documents\NVIDIA\scriptsAndTools\batch
REM SET PATH=%PATH%;C:\NVPACK\android-sdk-windows\platform-tools

REM ***********************************************************
REM Script to check Shield device information for bug reporting
REM ASSUMES adb.exe is already part of PATH variable (handled by TADP install)
REM jsansait@nvidia.com
REM ***********************************************************

SET device=0
SET deviceType=0
SET buildInfo=0
SET nvidiaVersion=0
SET controllerFW=0

	REM Usage with multiple devices connected is 'adb -s %serialno% shell'
	REM message: error: "more than one device/emulator"

	REM next step: check if multiple devices. prompt user to specify them
	
REM ***Check device connected***

adb devices -l | find "device product:" >nul
if errorlevel 1 ( 
	echo No devices found 
	GOTO:theend
	)

REM ***Check device model***

FOR /F %%a in ('adb shell getprop ro.product.name') do ( SET device=%%a )

IF /I %device% EQU wx_un_do ( SET device=ST8 )
IF /I %device% EQU wx_na_do ( SET device=ST8 )
IF /I %device% EQU wx_na_wf ( SET device=ST8 )
IF /I %device% EQU sb_na_wf ( SET device=Songbird )
IF /I %device% EQU foster_e ( SET device=FosterBase )
IF /I %device% EQU foster_e_hdd ( SET device=FosterPro )
IF /I %device% EQU darcy ( SET device=Darcy )

REM ***Check whether ATV or tablet, the list build and SW version***

FOR /F %%a in ('adb shell getprop ro.build.characteristics') do ( SET deviceType=%%a )
FOR /F "tokens=*" %%a in ('adb shell getprop ro.build.display.id') do ( SET buildInfo=%%a )
FOR /F %%a in ('adb shell getprop ro.build.version.ota') do ( SET nvidiaVersion=%%a )

REM ***Check controller info***

	REM adb shell dumpsys bluetooth_manager | grep -o "NVIDIA Controller v01.*" | grep -o "v01.*" > temp.txt
	REM SET /p controllerFW=<temp.txt

ECHO Device: %device%
ECHO Build Info: %buildInfo%
IF /I %deviceType% EQU tv ECHO Shield Android TV SW: %nvidiaVersion%
IF /I %deviceType% EQU tablet ECHO Shield Tablet SW: %nvidiaVersion%
	REM ECHO TS Firmware: %controllerFW%
REM DEL temp.txt

:theend
