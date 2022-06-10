echo > .exe_identifier
break> .exe_identifier

echo This file exists so that a potential .exe file can verify that it, in fact, is an .exe >> .exe_identifier
echo file. It does this by checking if this file exists in its `.` directory. If it does, it >> .exe_identifier
echo means that it's been build inside of the .exe ... or that someone has placed it in its >> .exe_identifier
echo directory. Until we find a better solution, just don't name anything `exe_identifier`, and >> .exe_identifier
echo then place it in the program's `.` directory... >> .exe_identifier