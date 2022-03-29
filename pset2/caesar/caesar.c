#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
//Validating the key
    if (argc != 2)
    {
        printf("Usage: ./ceasar key\n");
        return 1;
    }
    else
    {
        for (int j = 0; j < strlen(argv[1]); j++)
        {
            if (isdigit(argv[1][j]) == 0)
            {
                printf("Usage: ./ceasar key\n");
                return 1;
                break;
            }
            
        }

    }
    int counter = 0;
//checking if argument is digits. If so, printing success and converting the arg to an int
    int k;
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]) != 0)
        {
            counter++;
        }
    }
    if (counter > 0) //if the number of digits is more than 0
    {
        k = atoi(argv[1]); //make the argument an integer
            
        string plain = get_string("Plaintext: ");


        for (int s = 0; s < strlen(plain); s++)
        {
            
            if (isalpha(plain[s]) != 0 && isupper(plain[s]) != 0)
            {
                plain[s] -= 65; //setting the capitalized letters to 0
                plain[s] += k;
                plain[s] = plain[s] % 26; //applying the formula
                plain[s] += 65; //resetting the letters
        
            }
            else if (isalpha(plain[s]) != 0 && isupper(plain[s]) == 0)
            {
                plain[s] -= 97; //resetting the lower case letter
                plain[s] += k;
                plain[s] = plain[s] % 26; //formula
                plain[s] += 97; //resetting the letters
            }
        }
        
        printf("ciphertext: %s\n", plain);
        return 0; 
    }

   
    
}