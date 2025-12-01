# Expense Tracker Application

This project contains two versions of an Expense Tracker: a Web Application and a Desktop Application.

## Prerequisites

1.  **Install Python 3.12 or 3.13**: Download and install **Python 3.12** or **3.13** from [python.org](https://www.python.org/downloads/).
    *   **Reason**: Version 3.14 is experimental and does not work with this app.
    *   **IMPORTANT**: During installation, check the box that says **"Add Python to PATH"**.

## How to Run

### Option 1: Using the Run Script (Recommended)

1.  Double-click the `run.bat` file in this directory.
2.  **First Time Setup**: Type `3` and press Enter to install/update required libraries.
3.  **Run App**:
    *   Type `1` to run the Web Application (Streamlit).
    *   Type `2` to run the Desktop Application.

### Option 2: Running Manually

**Web Application (Streamlit):**
Run the following command in your terminal:
```bash
streamlit run web_app.py
```
This will open the application in your default web browser.

**Desktop Application (wxPython):**
Run the following command in your terminal:
```bash
python main.py
```
This will open the application in a new window.

## Troubleshooting
*   If the `run.bat` window closes immediately or you see an error, try running **Option 3** again to ensure all dependencies are installed.
*   Ensure you have an internet connection for the first run to download dependencies.
