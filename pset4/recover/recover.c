#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>
#define BLOCK 512

typedef uint8_t BYTE;

bool jpgSignature(BYTE buffer[])
{
    return (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0);
}

int main(int argc, char *argv[])
{
    bool jpgSignature(BYTE buffer[]);

    if (argc  != 2)
    {
        printf("Usage: ./recover image \n");
        return 1;
    }
    
    //open image and create buffer
    FILE *input = fopen(argv[1], "r");
    BYTE buffer[BLOCK];
    
    //if image is null, break and return 1
    if (input == NULL)
    {
        printf("Image cannot be opened for reading. \n");
        return 1;
    }
    //read first block
    fread(buffer, BLOCK, 1, input);
    
    FILE *image;
    int number = 0;
    
    char *filenames;
    filenames = malloc(400 * sizeof(int));
    
    bool openFile = false;
    
    
    while (fread(buffer, BLOCK, 1, input))
    {
        //if found jpeg
        if (jpgSignature(buffer))
        {
            //check if there's an open file already
            if (openFile)
            {
                fclose(image);
                openFile = false;
            }
            
            //set the name of new file and open it
            sprintf(filenames, "%03i.jpg", number);
            image = fopen(filenames, "w");
            number++;
            openFile = true;
            //check if new created file workds
            if (image == NULL)
            {
                return 1;
            }
                
            fwrite(buffer, BLOCK, 1, image);
        }
        else if (openFile)
        {
            fwrite(buffer, BLOCK, 1, image);
        }
        
    }
    
    fclose(image);
    fclose(input);
    //making sure malloc'd memory is freed
    free(filenames);
    
    return 0;
}
