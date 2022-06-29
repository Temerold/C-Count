:: ! IMPORTANT: Remember to run the this file when any program file is altered, to build
:: ! the project into `C-Count.exe`

gcc count.c -o count

echo > .exe_identifier
break> .exe_identifier
echo This file exists so that a potential .exe file can verify that it, in fact, is an .exe>> .exe_identifier
echo file. It does this by checking if this file exists in its `.` directory. If it does, it>> .exe_identifier
echo means that it's been built inside of the .exe ... or that someone has placed it in its>> .exe_identifier
echo directory. Until we find a better solution, just don't name anything `.exe_identifier`, and>> .exe_identifier
echo then place it in the program's directory...>> .exe_identifier

pyinstaller ^
--onefile ^
--icon=../src/logo.ico ^
--add-data ../src/logo.ico;. ^
--add-data ../src/on_small.png;. ^
--add-data ../src/off_small.png;. ^
--add-data count.exe;. ^
--add-data .exe_identifier;. ^
--clean ^
gui.py

del .exe_identifier
del gui.spec
cd dist
del C-Count.exe
rename gui.exe C-Count.exe
cd ..
rmdir /s /q build
rename dist build