@echo off
setlocal enabledelayedexpansion
set TYPE=%1
set SCOPE=%2
shift
shift
set MSG=%*
if "%TYPE%"=="" goto usage
if "%SCOPE%"=="" goto usage
if "%MSG%"=="" goto usage

git add -A
git commit -m "%TYPE%(%SCOPE%): %MSG%"
exit /b 0

:usage
echo Usage: scriptscommit-main.bat ^<type^> ^<scope^> ^<message...^>
echo type: feat^|fix^|refactor^|docs^|test^|chore
exit /b 1
