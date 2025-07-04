@echo off
echo Installing required libraries for Team 5 App...
echo.

REM Python 가상환경 생성 (선택사항)
echo Creating virtual environment...
python -m venv venv
echo.

REM 가상환경 활성화
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM 라이브러리 설치
echo Installing libraries from requirements.txt...
pip install -r requirements.txt
echo.

echo Installation completed!
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run the app: streamlit run main.py
echo.
pause 