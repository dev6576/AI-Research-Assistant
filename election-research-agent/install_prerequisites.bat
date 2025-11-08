@echo off
echo Installing prerequisites for llama-cpp-python...

:: Download VS Build Tools installer
echo Downloading Visual Studio Build Tools...
curl -L -o vs_buildtools.exe https://aka.ms/vs/17/release/vs_buildtools.exe

:: Install VS Build Tools (C++ workload)
echo Installing Visual Studio Build Tools...
vs_buildtools.exe --quiet --wait --norestart --nocache ^
    --installPath "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools" ^
    --add Microsoft.VisualStudio.Workload.NativeDesktop ^
    --includeRecommended

:: Download and install CMake
echo Downloading CMake...
curl -L -o cmake-installer.msi https://github.com/Kitware/CMake/releases/download/v3.27.7/cmake-3.27.7-windows-x86_64.msi

echo Installing CMake...
msiexec /i cmake-installer.msi /quiet /norestart

:: Clean up installers
del vs_buildtools.exe
del cmake-installer.msi

echo Installation complete. Please restart your terminal and try pip install again.
pause