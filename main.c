#include <stdio.h>
#include <stdlib.h>

void count(int start, int end)
{
    if (end < start && end != -1) //´start´ is greater than ´end´ (´end´ can however be -1, which means infinity).
    {
        printf("Error: Start integer can't be greater than end integer!\n");
        exit(2);
    }
    else if (start < 0) // ´start´ is negative
    {
        printf("Error: Start integer can't be a negative number!\n");
        exit(2);
    }
    else if (end < 0 && end != -1) // ´end´ is negative (it can however be -1, which means infinity )
    {
        printf("Error: End integer can't be a negative number (except for -1, which means infinity)!\n");
        exit(2);
    }

    // Start counting at ´start´, and end at ´end´. If ´end´ is -1, the program will continue forever.
    for (int num = start; num <= (end) || end == -1; ++num)
    {
        printf("\n%d", num);
    }
}

int main(int argc, char *argv[])
{
    if (argc > 3) // More than 3 arguments
    {
        printf("Error: Too many arguments! The maximum is 2; start integer and end integer.\n");
        exit(2);
    }
    else if (argc < 3) // Less than 3 arguments
    {
        printf("Error: Missing argument(s)! Requires both start integer and end integer.\n");
        exit(2);
    }
    char *start_param = argv[1];
    char *end_param = argv[2];
    int start = atoi(start_param); // Convert str to int
    int end = atoi(end_param);     // Convert str to int

    count(start, end);
}
