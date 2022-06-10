# ! IMPORTANT: Remember to run the this file when any program file is altered, to build
# ! the project into `C-Count-Linux.exe`

sudo gcc count-linux.c -o count-linux.exe

sudo touch exe_identifier.txt

echo "This file exists so that a potential .exe file can verify that it, in fact, is an .exe" >> exe_identifier.txt
echo "file. It does this by checking if this file exists in its `.` directory. If it does, it" >> exe_identifier.txt
echo "means that it's been built inside of the .exe ... or that someone has placed it in its" >> exe_identifier.txt
echo "directory. Until we find a better solution, just don't name anything `exe_identifier.txt`," >> exe_identifier.txt
echo "and then place it in the program's directory..." >> exe_identifier.txt

sudo pyinstaller --onefile --icon=../src/logo.ico --add-data ../src/logo.ico:. --add-data ../src/on_small.png:. --add-data ../src/off_small.png:. --add-data count-linux.exe:. --add-data exe_identifier.txt:. --clean --exclude-module _bootlocale gui-linux.py