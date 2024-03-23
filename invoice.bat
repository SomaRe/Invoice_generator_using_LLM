@echo off

rem Change to the directory where your script and virtual environment are located
cd /d "%~dp0" 

rem Activate the virtual environment
call venv\Scripts\activate.bat


rem Run the Python script with the provided message
python invoice.py "%~1"