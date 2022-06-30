:: ! IMPORTANT: Remember to run the this file when any program file is altered, to build
:: ! the project into `C-Count.exe`

gcc count.c -o count

pyinstaller ^
--onefile ^
--icon=../media/logo.ico ^
--add-data ../media/logo.ico;. ^
--add-data ../media/on_small.png;. ^
--add-data ../media/off_small.png;. ^
--add-data count.exe;. ^
--clean ^
gui.py

del gui.spec
cd dist
del C-Count.exe
rename gui.exe C-Count.exe
cd ..
rmdir /s /q build
rename dist build
