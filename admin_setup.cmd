@echo off
REM ----------------------------------------------------------------------
REM |
REM |  admin_setup.cmd
REM |
REM |  David Brownell <db@DavidBrownell.com>
REM |      2020-11-15 09:59:27
REM |
REM ----------------------------------------------------------------------
REM |
REM |  Copyright David Brownell 2020-21
REM |  Distributed under the Boost Software License, Version 1.0. See
REM |  accompanying file LICENSE_1_0.txt or copy at
REM |  http://www.boost.org/LICENSE_1_0.txt.
REM |
REM ----------------------------------------------------------------------
REM Setup activities that require admin access

if %1 NEQ "" (
    if %2 NEQ "" (
        goto EndArgValidation
    )
)

echo.
echo ERROR: Usage - %0 ^<Existing User Dir^> ^<New User Dir^>
echo.
exit /B -1

:EndArgValidation

REM Create the link
if not exist %2 (
    mklink /J /D %2 %1
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Unable to create link
        exit /B %ERRORLEVEL%
    )
)

REM Activate the environment
call "%~dp0\Activate.cmd"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Unable to activate the environment
    exit /B %ERRORLEVEL%
)

REM Update the configuration
echo RUNNING 'npm config set cache "%2\AppData\Roaming\npm-cache" --global'...
call npm config set cache "%2\AppData\Roaming\npm-cache" --global
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Unable to update the npm configuration
    exit /B %ERRORLEVEL%
)

REM Create the configuration file
(
echo This file is used to communicate that admin_setup has been run and completed successfully. Please do not remove this file, as it will cause other tools to prompt you to run admin_setup.cmd again.
echo.
echo     - npx for username with spaces
echo.
) > "%~dp0admin_setup.complete"

REM Indicate success
echo.
echo.
echo The setup activities were successful - you may close this command prompt.
echo.
echo.
