@echo off
setlocal enabledelayedexpansion
set SCOPE=%1
shift
set MSG=%*
if "%SCOPE%"=="" goto usage
if "%MSG%"=="" goto usage

git add -A
git commit -m "checkpoint(%SCOPE%): %MSG%"
exit /b 0

:usage
echo Usage: scriptscommit-checkpoint.bat ^<scope^> ^<message...^>
exit /b 1
