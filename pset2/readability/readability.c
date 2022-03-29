#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int main(void)
{
    //prompting user for text
    string txt = get_string("Text:");
    //initiating counters. Word is assigned to 1, since the last one wouldn't be counted as it has no space after
    int lettercount = 0;
    float wordcount = 1;
    int sentences = 0;
    //treating the string as an array of chars, using a loop + bool to check if it's letter, space or punctuation
    for (int i = 0; i < strlen(txt); i++)
    {
        if ((txt[i] >= 65 && txt[i] <= 90) || (txt[i] >= 97 && txt[i] <= 122))
        {
            lettercount++;
        }

        else if (txt[i] == 32)
        {
            wordcount++;
        }

        else if (txt[i] == 46 || txt[i] == 33 || txt[i] == 63)
        {
            sentences++;
        }
    }
//getting the value that makes wordcount == 100. Multiplying letters and sentences by Y to get the avg per 100
    float Y = 100 / wordcount;
    float L = Y * lettercount;
    float S = Y * sentences;
//Coleman-Liau index
    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = round(index);
//printing out the correct value
    if (index > 0 && index < 16)
    {
        printf("Grade %.0f\n", index);
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index <= 0)
    {
        printf("Before Grade 1\n");

    }
}
