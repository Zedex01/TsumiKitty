@Echo off
:: Goto Current .Bat file
cd /d %~dp0

::Delete old build
IF EXIST build ( rmdir build /s /q )
IF EXIST dist ( rmdir dist /s /q )
IF EXIST Tsumikitty.spec ( del Tsumikitty.spec )

::Check for arguments
IF "%1" == "" (
    echo Building without console...
    pyinstaller --name Tsumikitty --onedir --noconsole --add-data "data;data" --paths src main.py
    
    REM Copy over Config and DB files
    xcopy "data" "dist\Tsumikitty\data" /E /I /Y
    exit
)
IF "%1" == "-c" (
    echo Building with console...
    pyinstaller --name Tsumikitty --onedir --add-data "data;data" --paths src main.py
    
    REM Copy over Config and DB files
    xcopy "data" "dist\Tsumikitty\data" /E /I /Y
    exit
)
IF "%1" == "-clean" (
    echo Cleanup Done!
    exit
)