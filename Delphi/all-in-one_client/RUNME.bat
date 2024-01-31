@echo off
CLS

echo.
echo.
echo Running DELPHI installer.
echo.
echo.
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Running without administrative privileges
    pause
    exit
)                         
ping localhost -n 2 >nul

echo                                     .                                                    
ping localhost -n 1.5 >nul
echo                                   .---                                                   
ping localhost -n 1.5 >nul
echo                                   -----                                                  
ping localhost -n 1.5 >nul
echo                                  -------                                                 
ping localhost -n 1.5 >nul
echo                                 --------=.                                               
ping localhost -n 1.5 >nul
echo                                :---------=:                                              
ping localhost -n 1.5 >nul
echo                               :--:--------=:                                             
ping localhost -n 1.5 >nul
echo                              .--::---------=-                                            
ping localhost -n 1.5 >nul
echo                              --:::---------==-                                           
ping localhost -n 1.5 >nul
echo                             ---:::----------==-                                          
ping localhost -n 1.5 >nul
echo                            ---:::------------===.                                        
ping localhost -n 1.5 >nul
echo                           :--::::-------------===.                                       
ping localhost -n 1.5 >nul
echo                          :--:::::--------------===:                                      
ping localhost -n 1.5 >nul
echo                         :=-::::::---------------===:                                     
ping localhost -n 1.5 >nul
echo                        :=--:::::-----------------===-                                    
ping localhost -n 1.5 >nul
echo                       :=--::::::------------------===-                                   
ping localhost -n 1.5 >nul
echo                      :=--:::::::-------------------===-.                                 
ping localhost -n 1.5 >nul
echo                     :=--:::::::--------------------=====.                                
ping localhost -n 1.5 >nul
echo                    :==--:::::::---------------------=====.                               
ping localhost -n 1.5 >nul
echo                   :==--::::::::----------------------=====:                              
ping localhost -n 1.5 >nul
echo                  :==--:::::::::-----------------------=====:                             
ping localhost -n 1.5 >nul
echo                 .==--:::::::::-------------------------=====-                            
ping localhost -n 1.5 >nul
echo                .==--::::::----========================-======-                           
ping localhost -n 1.5 >nul
echo    ==-::.     .==---:-----====================================-                          
ping localhost -n 1.5 >nul
echo    .=======:::===------==============+#=:-========-::=*========-                         
ping localhost -n 1.5 >nul
echo      ==========------============-. :@@#  .======-   @@+ -======-                        
ping localhost -n 1.5 >nul
echo       -=========----=============:  .+#+--====++==-::*%=..-======.                       
ping localhost -n 1.5 >nul
echo        -=========---===========================++================.                       
ping localhost -n 1.5 >nul
echo         -=========--============================+++==============.                       
ping localhost -n 1.5 >nul
echo          -=========-============================++++============+.                       
ping localhost -n 1.5 >nul
echo           -========-==========================+++++==============                        
ping localhost -n 1.5 >nul
echo            :====================================================-                        
ping localhost -n 1.5 >nul
echo             .==============================+###########*========                         
ping localhost -n 1.5 >nul
echo              .=====================++*####%%#%%%%******+==========:                         
ping localhost -n 1.5 >nul
echo               :===============================================-                          
ping localhost -n 1.5 >nul
echo                -+=============================================                           
ping localhost -n 1.5 >nul
echo                 -+===========================================.                           
ping localhost -n 1.5 >nul
echo                  =+=========================================.                            
ping localhost -n 1.5 >nul
echo                   =+=======================================.                             
ping localhost -n 1.5 >nul
echo                    -++====================================.                              
ping localhost -n 1.5 >nul
echo                     =+++++++++==++===================++==                                
ping localhost -n 1.5 >nul
echo                     -+++++++++++++++++++++++++++++++++++:                                
ping localhost -n 1.5 >nul
echo                     =+++++++++++++++++++++++++++++++++++.                                
ping localhost -n 1.5 >nul
echo                    -==-====+++++++++++++++++++++++++++++-                                
ping localhost -n 1.5 >nul
echo                  .==-------------=========================:                              
ping localhost -n 1.5 >nul
echo                 :==--------------------------==============-                             
ping localhost -n 1.5 >nul
echo                -==---------------------------================:                           
ping localhost -n 1.5 >nul
echo              :===----------------------------=================-.                         
ping localhost -n 1.5 >nul
echo             -===-----------------------------===================:                        
ping localhost -n 1.5 >nul
echo           :===-------------------------------====================-.                      
ping localhost -n 1.5 >nul
echo         .-===---------------------------------=====================-                     
ping localhost -n 3 >nul

echo.
echo.

:: Get the directory of the batch script
set SCRIPT_DIR=%~dp0

:: Change the current directory to the script directory
cd /d "%SCRIPT_DIR%"

goto start

:: Function to check and install software
:check_and_install
echo Checking for %1...
reg query %2 >nul 2>nul
set regCheckErrorLevel=%errorLevel%
echo Registry query completed for %1 with error level: %regCheckErrorLevel%
if %regCheckErrorLevel% neq 0 (
    echo %1 is not installed. Installing %1...
    call :install_software %1 %3
) else (
    echo %1 is already installed.
)
goto :eof

:install_software
echo Installing %1...

:: Save the current directory and then change to the installers directory
pushd "%~dp0installers"

if "%~x2"==".msi" (
    msiexec /i "%2" /quiet
) else (
    %2 /S
)
if %errorLevel% neq 0 (
    pause 
    exit /b
)

:: Return to the original directory
popd

echo %1 installed successfully.
cd ..
goto :eof

:start
:: Install Node.js
if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    call :check_and_install Node.js "HKLM\Software\Node.js" node-v20.11.0-x86.msi
) else (
    call :check_and_install Node.js "HKLM\Software\Node.js" node-v20.11.0-x64.msi
)
:: Install IrfanView
if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    call :check_and_install IrfanView "HKLM\Software\IrfanView" iview466_setup
) else (
    call :check_and_install IrfanView "HKLM\Software\IrfanView" iview466_x64_setup.exe
)

if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    call :check_and_install Python "HKLM\Software\Python\PythonCore\3.12-32" python-3.12.1.exe
) else (
    call :check_and_install Python "HKLM\Software\Python\PythonCore\3.12" python-3.12.1-amd64.exe
)
echo Installation process completed.

for /f "tokens=2,*" %%a in ('reg query "HKLM\Software\Node.js" /v "InstallPath" 2^>nul') do set nodePath=%%b
if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    for /f "tokens=2,*" %%a in ('reg query "HKLM\Software\Python\PythonCore\3.12-32\InstallPath" /v "ExecutablePath" 2^>nul') do set pythonPath=%%b
) else (
    for /f "tokens=2,*" %%a in ('reg query "HKLM\Software\Python\PythonCore\3.12\InstallPath" /v "ExecutablePath" 2^>nul') do set pythonPath=%%b
)

:: Install vite using npm
echo Installing NodeJS dependency
call "%nodePath%\node.exe" "%nodePath%\node_modules\npm\bin\npm-cli.js" install -g vite

:: Start http-server in the dist directory within the "requirements" folder
echo Starting up local server
start vite preview

%pythonPath% -m pip install -r "%SCRIPT_DIR%\python\requirements.txt"

echo Starting up Python printer service in virtual env...
%pythonPath% "%SCRIPT_DIR%\python\main.py"

pause
exit