@echo off
adb kill-server
adb server start
echo adb restarted
pause