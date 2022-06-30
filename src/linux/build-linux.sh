# ! IMPORTANT: Remember to run the this file when any program file is altered, to build
# ! the project into `C-Count-Linux.exe`

sudo gcc count-linux.c -o count-linux.exe

sudo pyinstaller \
--onefile \
--icon=../media/logo.ico \
--add-data ../media/logo.ico:. \
--add-data ../media/on_small.png:. \
--add-data ../media/off_small.png:. \
--add-data count-linux.exe:. \
--clean \
--exclude-module _bootlocale \
gui-linux.py
