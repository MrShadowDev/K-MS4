@echo off
echo Installing required Python packages...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    exit /b
)

pip install os re json asyncio aiohttp tkinter requests >nul 2>&1

if %errorlevel% neq 0 (
    echo Failed to install the required Python packages. Ensure pip is working correctly.
    exit /b
)

echo Running the Python script...
python main.py

pause
