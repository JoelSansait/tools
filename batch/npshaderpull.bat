@ECHO off
SET PATH=%PATH%;C:\Users\jsansait\Documents\NVIDIA\scriptsAndTools\batch

if [%1]==[] goto arginvalid

adb pull /sdcard/Android/obb/com.nvidia.nintendo.%1/%1_ShaderCache.dat
goto:eof

:arginvalid
echo "Usage npshaderpull <game prefix>"
