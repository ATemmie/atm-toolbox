@echo off
rem ATM 工具箱 - Go 套餐数据自动更新（静默运行）
cd /d "C:\Users\Administrator\Desktop\传输\projects\atm-toolbox"
"C:\Users\Administrator\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" update_go.py --push >> update_log.txt 2>&1