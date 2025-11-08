@echo off
echo Setting up Python environment...

:: Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

:: Set environment variables for llama-cpp-python build
set CMAKE_ARGS=-DLLAMA_CUBLAS=off
set FORCE_CMAKE=1

:: Install packages with specific configurations
pip install --upgrade pip
pip install wheel setuptools
pip install cmake
pip install llama-cpp-python==0.2.11 --no-cache-dir --verbose

:: Install remaining requirements
pip install -r requirements.txt

echo Installation complete!
pause