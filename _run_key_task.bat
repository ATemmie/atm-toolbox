@echo off
schtasks /Delete /TN AddLaptopKey /F 2>nul
schtasks /Create /TN AddLaptopKey /TR "powershell -ExecutionPolicy Bypass -File C:\add_laptop_key.ps1" /SC ONCE /ST 00:00 /RL HIGHEST /F /RU SYSTEM
schtasks /Run /TN AddLaptopKey
timeout /t 5 /nobreak >nul
schtasks /Query /TN AddLaptopKey /FO LIST 2>nul
echo DONE