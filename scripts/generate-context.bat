@echo off
setlocal enabledelayedexpansion
set BASE_BRANCH=%1
if "%BASE_BRANCH%"=="" set BASE_BRANCH=main
set OUT=%2
if "%OUT%"=="" set OUT=.mcpcontext_incremental.txt

if not exist .mcp mkdir .mcp

echo # AI Development System Context (Incremental / Onion Model)> "%OUT%"
echo.>> "%OUT%"

for %%F in (docsARCHITECTURE.md docsCONVENTIONS.md) do (
  if exist %%F (
    echo === %%F ===>> "%OUT%"
    type %%F>> "%OUT%"
    echo.>> "%OUT%"
  )
)

for /f "delims=" %%A in ('dir /b /o-d docsadrADR-*.md 2^>nul') do (
  echo --- docsadr%%A --->> "%OUT%"
  type docsadr%%A>> "%OUT%"
  echo.>> "%OUT%"
  goto afteradr
)
:afteradr

echo === git diff %BASE_BRANCH%...HEAD ===>> "%OUT%"
git diff %BASE_BRANCH%...HEAD>> "%OUT%" 2>nul
echo.>> "%OUT%"

for /f "delims=" %%F in ('git diff --name-only %BASE_BRANCH%...HEAD 2^>nul') do (
  if exist %%F (
    echo === %%F ===>> "%OUT%"
    type %%F>> "%OUT%"
    echo.>> "%OUT%"
  )
)

echo Wrote incremental context: %OUT%
