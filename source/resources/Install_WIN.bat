@ECHO OFF

ECHO "Initializing"
SET extPath="%APPDATA%\espanso\match\packages\good-morning"

ECHO "Removing any existing extension data"
IF EXIST %extPath% RMDIR %extPath% /s /q

ECHO "Creating extension directory"
MKDIR %extPath%

ECHO "Installing extension"
XCOPY ..\ %extPath% /s /exclude:installExclusions.txt

ECHO "Cleaning up"
DEL "%extPath%\resources\Install_*"

ECHO "Finished"

