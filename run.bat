@echo off
setlocal
title Expense Tracker Launcher

:MENU
cls
echo ==========================================
echo       Expense Tracker Launcher
echo ==========================================
echo.
python --version
echo.
echo NOTE: If you see "Python 3.14", please uninstall it and install Python 3.12 or 3.13.
echo.
echo 1. Run Web Application (Streamlit)
echo 2. Run Desktop Application (wxPython)
echo 3. Install/Update Dependencies (Run this first!)
echo 4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto WEB
if "%choice%"=="2" goto DESKTOP
if "%choice%"=="3" goto INSTALL
if "%choice%"=="4" goto EXIT

echo Invalid choice. Please try again.
pause
goto MENU

:WEB
cls
echo Starting Web Application...
echo.
python -m streamlit run web_app.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application crashed.
    echo Possible causes:
    echo  - Python is not installed.
    echo  - Dependencies are not installed (Try Option 3).
    echo.
    pause
)
goto MENU

:DESKTOP
cls
echo Starting Desktop Application...
echo.
python main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application crashed.
    echo Possible causes:
    echo  - Python is not installed.
    echo  - Dependencies are not installed (Try Option 3).
    echo.
    pause
)
goto MENU

:INSTALL
cls
echo Installing Dependencies...
echo.
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies.
    echo Make sure Python is installed and added to PATH.
    echo.
) else (
    echo.
    echo Dependencies installed successfully!
)
pause
goto MENU

:EXIT
exit
