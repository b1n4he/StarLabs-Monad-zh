@echo off
echo Checking virtual environment...

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing requirements...
    call venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple    

)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting StarLabs Monad Bot...
python main.py
pause
