#if _WIN32_WINNT < 0x0500
#undef _WIN32_WINNT
#define _WIN32_WINNT 0x0500
#endif

#include <stdio.h>
#include <stdlib.h>

#include <windows.h>
#include <ctype.h>
#include <conio.h>

// ! IMPORTANT: Remember to run the `compile.bat` script when `count.c` (this file) is
// ! altered -- to compile it -- and then add the .exe (`C-Count.exe`) file to the Git
// ! commit!

void pause()
{
    printf("Press any key to continue . . .");
    getch(); // Wait for key input, then continue
}

void error(char *msg)
{
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    // Save terminal text attributes, to later revert back to them
    CONSOLE_SCREEN_BUFFER_INFO consoleInfo;
    GetConsoleScreenBufferInfo(hConsole, &consoleInfo);
    WORD saved_attributes = consoleInfo.wAttributes;

    // Set terminal text color to red
    SetConsoleTextAttribute(hConsole, FOREGROUND_RED);

    printf(msg); // Print error message

    SetConsoleTextAttribute(hConsole, // Revert terminal text to its original attributes
                            saved_attributes);

    pause();
    exit(2);
}

int validate_nums(unsigned long start, unsigned long end)
{
    // `start` greater than `end` (-1 meaning infinity; then start's smaller)
    if (start < end && end != -1)
    {
        error("ERROR: Invalid input! Start integer can't be greater than end integer.\n");
    }
    else if (start < 1) // `start` not positive
    {
        error("ERROR: Invalid input! Start integer must be a positive number.\n");
    }
    else if (end < 1 && end != -1) // `end` not positive or -1 (infinity)
    {
        error("ERROR: Invalid input! End integer must be a positive number (or -1, "
              "meaning infinity).\n");
    }
}

void count(unsigned long start, unsigned long end)
{
    // `validate_nums()` exits the program with an error code of 2 if an error is
    // encountered. If nothing's wrong, it does nothing.
    validate_nums(start, end);

    // Here, we have this if-else statement, with different code based on if `end` is -1
    // or not. Yes, we could just have one single for loop, which would continue forever
    // if `end` is -1. That, however, would be inefficient; checking if `end` is -1 every
    // recursion -- it's not going to change, so why check? Instead, we have a separate
    // never-ending while loop if `end` is -1, and it'll never stop and check `end`'s
    // value.
    if (end == -1)
    {
        unsigned long num = start;
        while (1)
        {
            printf("\n#%d", num);
            num += 1;
        }
    }
    else
    {
        for (unsigned long num = start; num <= end; num++)
        {
            printf("\n%d", num);
        }
    }
}

int is_integer(char s[])
{
    if (strcmp(s, "-1") == 0) // String doesn't equal "-1"
    {
        return 1;
    }

    // Loop through characters, return 0 if non-integer found
    for (int i = 0; s[i] != '\0'; i++)
    {
        if (!isdigit(s[i]))
        {
            return 0;
        }
    }
    return 1;
}

// This function runs automatically every time the program is ran. If the program is ran
// as a standalone, it will run without a GUI, asking for a start and end number.
// * In Visual Studio Code, the following line might get marked as an error, but it
// * compiles and runs correctly. This is a documented bug:
// * https://developercommunity.visualstudio.com/t/cc-intellisense-in-gccclang-mode-shows-attribute-c/796872
void __attribute__((constructor)) start_up(void)
{
    SetConsoleTitle("C-Count");
    DWORD dwProcessId;
    GetWindowThreadProcessId(GetConsoleWindow(), &dwProcessId);
    if (GetCurrentProcessId() == dwProcessId) // Ran as standalone
    {
        unsigned long start, end;

        printf("Start at: ");
        scanf("%d", &start);
        printf("End at: ");
        scanf("%d", &end);

        count(start, end);
        pause();
        exit(0);
    }
}

int main(int argc, char *argv[])
{
    if (argc > 3) // More than two arguments
    {
        error("ERROR: Too many arguments! The maximum is 2; start integer and end "
              "integer.\n");
    }
    else if (argc < 3) // Fewer than two arguments
    {
        error("ERROR: Missing argument(s)! Requires both start integer and end integer."
              "\n");
    }
    else if (!is_integer(argv[1]))
    {
        error("ERROR: Invalid input! Start integer must be entirely numerical.\n");
    }
    else if (!is_integer(argv[2]))
    {
        error("ERROR: Invalid input! End integer must be entirely numerical.\n");
    }

    char *ptr;
    // Convert chars to 64 bit ints
    long start = strtoll(argv[1], &ptr, 10);
    long end = strtoll(argv[2], &ptr, 10);
    count(start, end);
    exit(0);
}
